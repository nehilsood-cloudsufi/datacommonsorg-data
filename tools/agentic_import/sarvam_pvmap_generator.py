#!/usr/bin/env python3

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PV Map generator using Sarvam AI API instead of Gemini CLI.

This script is functionally equivalent to pvmap_generator.py but uses the
Sarvam AI REST API (OpenAI-compatible) rather than the Gemini CLI agent.
It implements its own agentic loop: generate pvmap/metadata → run statvar
processor → feed errors back → repeat.

Usage:
    python sarvam_pvmap_generator.py \
        --input_data=sample_data.csv \
        --sarvam_api_key=YOUR_KEY \
        --model=sarvam-30b \
        --output_path=output/output

Or set SARVAM_API_KEY env variable instead of --sarvam_api_key.
"""

import copy
import os
import platform
import random
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from absl import app
from absl import flags
from absl import logging
from jinja2 import Environment, FileSystemLoader

_FLAGS = flags.FLAGS
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_SARVAM_BASE_URL = "https://api.sarvam.ai/v1"
_DEFAULT_MODEL = "sarvam-30b"
_MAX_DATA_SAMPLE_LINES = 20
_MAX_METADATA_BYTES = 65536


def _define_flags():
    try:
        flags.DEFINE_list('input_data', None,
                          'List of input data file paths (required)')
        flags.mark_flag_as_required('input_data')

        flags.DEFINE_list('input_metadata', [],
                          'List of input metadata file paths (optional)')

        flags.DEFINE_list(
            'extra_instruction_files', [],
            'List of extra instruction file paths (optional)')

        flags.DEFINE_boolean(
            'sdmx_dataset', False,
            'Whether the dataset is in SDMX format (default: False)')

        flags.DEFINE_boolean('dry_run', False,
                             'Generate prompt only without calling Sarvam API')

        flags.DEFINE_string('maps_api_key', None,
                            'Google Maps API key (optional)')

        flags.DEFINE_string('dc_api_key', None,
                            'Data Commons API key (optional)')

        flags.DEFINE_integer(
            'max_iterations', 10,
            'Maximum number of refinement attempts.')

        flags.DEFINE_boolean(
            'skip_confirmation', False,
            'Skip user confirmation before starting PV map generation')

        flags.DEFINE_string(
            'output_path', 'output/output',
            'Output path prefix for all generated files (default: output/output)'
        )

        flags.DEFINE_string(
            'working_dir', None,
            'Working directory for the generator (default: current directory)')

        flags.DEFINE_integer(
            'extra_instruction_max_bytes', 65536,
            'Maximum allowed size in bytes for each extra instruction file')

        flags.DEFINE_string(
            'sarvam_api_key', None,
            'Sarvam AI API key. Falls back to SARVAM_API_KEY env variable.')

        flags.DEFINE_string(
            'model', _DEFAULT_MODEL,
            'Sarvam model to use: sarvam-m (30B) or sarvam-l (105B)')

        flags.DEFINE_boolean(
            'lite_prompt', True,
            'Use the compact Sarvam-optimised prompt template (default: True). '
            'Set to False to use the full DC knowledge-base prompt.')
    except flags.DuplicateFlagError:
        pass


@dataclass
class DataConfig:
    input_data: List[str]
    input_metadata: List[str]
    is_sdmx_dataset: bool = False


@dataclass
class Config:
    data_config: DataConfig
    dry_run: bool = False
    maps_api_key: str = None
    dc_api_key: str = None
    max_iterations: int = 10
    skip_confirmation: bool = False
    output_path: str = 'output/output'
    working_dir: Optional[str] = None
    extra_instruction_files: List[str] = field(default_factory=list)
    extra_instruction_max_bytes: int = _MAX_METADATA_BYTES
    sarvam_api_key: Optional[str] = None
    model: str = _DEFAULT_MODEL
    lite_prompt: bool = True


@dataclass
class GenerationResult:
    run_id: str
    run_dir: Path
    prompt_path: Path
    api_log_path: Path
    model: str
    success: bool = False


class SarvamPVMapGenerator:
    """PV map generator using Sarvam AI REST API."""

    def __init__(self, config: Config):
        self._working_dir = Path(
            config.working_dir).resolve() if config.working_dir else Path.cwd()
        if self._working_dir.exists() and not self._working_dir.is_dir():
            raise ValueError(
                f"working_dir is not a directory: {self._working_dir}")
        self._working_dir.mkdir(parents=True, exist_ok=True)

        self._config = copy.deepcopy(config)

        # Resolve API key
        self._api_key = (self._config.sarvam_api_key
                         or os.environ.get('SARVAM_API_KEY'))
        if not self._api_key and not self._config.dry_run:
            raise ValueError(
                "Sarvam API key required. Pass --sarvam_api_key or set "
                "SARVAM_API_KEY environment variable.")

        # Convert input_data paths to absolute
        if self._config.data_config.input_data:
            self._config.data_config.input_data = [
                self._validate_and_convert_path(p)
                for p in self._config.data_config.input_data
            ]

        # Convert input_metadata paths to absolute
        if self._config.data_config.input_metadata:
            self._config.data_config.input_metadata = [
                self._validate_and_convert_path(p)
                for p in self._config.data_config.input_metadata
            ]

        # Resolve extra instruction files
        if self._config.extra_instruction_files:
            self._config.extra_instruction_files = [
                self._validate_extra_instruction_file(p)
                for p in self._config.extra_instruction_files
            ]

        # Parse output path
        output_path_raw = self._config.output_path
        if not output_path_raw or not output_path_raw.strip():
            raise ValueError("output_path must be a non-empty string")
        output_path = Path(output_path_raw).expanduser()
        if len(output_path.parts) < 2:
            raise ValueError("output_path must include a directory and prefix")
        if not output_path.is_absolute():
            output_path = self._working_dir / output_path
        self._output_path_abs = output_path.resolve()
        self._output_dir_abs = self._output_path_abs.parent
        self._output_basename = self._output_path_abs.name
        self._config.output_path = str(self._output_path_abs)
        self._output_dir_abs.mkdir(parents=True, exist_ok=True)

        self._datacommons_dir = self._working_dir / '.datacommons'
        self._datacommons_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._run_id = (
            f"{self._output_basename}_sarvam_{timestamp}_{random.randint(1, 10000)}"
        )
        self._run_dir = self._datacommons_dir / 'runs' / self._run_id
        self._run_dir.mkdir(parents=True, exist_ok=True)

    def _validate_and_convert_path(self, path: str) -> Path:
        real_path = self._resolve_path(path)
        working_dir = self._working_dir.resolve()
        try:
            real_path.relative_to(working_dir)
        except ValueError:
            raise ValueError(
                f"Path '{path}' is outside working directory '{working_dir}'")
        return real_path

    def _resolve_path(self, path: str) -> Path:
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = self._working_dir / p
        return p.resolve()

    def _validate_extra_instruction_file(self, path: str) -> Path:
        resolved = self._resolve_path(path)
        if not resolved.exists():
            raise ValueError(f"Extra instruction file not found: {resolved}")
        if not resolved.is_file():
            raise ValueError(
                f"Extra instruction path is not a file: {resolved}")
        file_size = resolved.stat().st_size
        max_bytes = self._config.extra_instruction_max_bytes
        if file_size > max_bytes:
            raise ValueError(
                f"Extra instruction file larger than {max_bytes} bytes: {resolved}"
            )
        try:
            resolved.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raise ValueError(
                f"Extra instruction file is not valid UTF-8: {resolved}")
        return resolved

    def _read_data_sample(self) -> str:
        """Read first N lines of input data file."""
        data_file = self._config.data_config.input_data[0]
        lines = []
        with open(data_file, 'r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f):
                if i >= _MAX_DATA_SAMPLE_LINES:
                    break
                lines.append(line.rstrip('\n'))
        return '\n'.join(lines)

    def _read_metadata_files(self) -> List[dict]:
        """Read all metadata files, truncating large ones."""
        results = []
        for meta_path in self._config.data_config.input_metadata:
            try:
                content = meta_path.read_text(encoding='utf-8',
                                              errors='replace')
                if len(content.encode('utf-8')) > _MAX_METADATA_BYTES:
                    content = content.encode('utf-8')[:_MAX_METADATA_BYTES].decode(
                        'utf-8', errors='replace')
                    content += '\n... [truncated] ...'
                results.append({'path': str(meta_path), 'content': content})
            except Exception as e:
                logging.warning("Could not read metadata file %s: %s",
                                meta_path, e)
        return results

    def _read_extra_instruction_files(self) -> List[dict]:
        results = []
        for path in self._config.extra_instruction_files:
            try:
                content = path.read_text(encoding='utf-8')
                results.append({'path': str(path), 'content': content})
            except Exception as e:
                logging.warning("Could not read extra instruction file %s: %s",
                                path, e)
        return results

    def _render_prompt(self,
                       previous_error: Optional[str] = None,
                       previous_pvmap: Optional[str] = None,
                       previous_metadata: Optional[str] = None) -> str:
        """Render the API prompt template."""
        template_dir = os.path.join(_SCRIPT_DIR, 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template_name = (
            'generate_pvmap_sarvam_lite_prompt.j2'
            if self._config.lite_prompt else 'generate_pvmap_api_prompt.j2')
        template = env.get_template(template_name)

        tools_dir = os.path.abspath(os.path.join(_SCRIPT_DIR, '..'))

        template_vars = {
            'working_dir_abs': str(self._working_dir),
            'python_interpreter': sys.executable,
            'script_dir_abs': tools_dir,
            'input_data_abs': str(self._config.data_config.input_data[0]),
            'input_metadata_abs': [
                str(p) for p in self._config.data_config.input_metadata
            ],
            'dataset_type':
                'sdmx' if self._config.data_config.is_sdmx_dataset else 'csv',
            'sarvam_run_id': self._run_id,
            'output_path_abs': str(self._output_path_abs),
            'output_dir_abs': str(self._output_dir_abs),
            'output_basename': self._output_basename,
            'run_dir_abs': str(self._run_dir),
            'extra_instruction_files_abs': [
                str(p) for p in self._config.extra_instruction_files
            ],
            'input_data_sample': self._read_data_sample(),
            'input_metadata_contents': self._read_metadata_files(),
            'extra_instruction_files_contents':
                self._read_extra_instruction_files(),
            'previous_error': previous_error,
            'previous_pvmap': previous_pvmap,
            'previous_metadata': previous_metadata,
        }

        return template.render(**template_vars)

    def _call_api(self, prompt: str) -> str:
        """Call Sarvam AI API with the given prompt."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package required. Install with: pip install openai")

        client = OpenAI(api_key=self._api_key, base_url=_SARVAM_BASE_URL)
        logging.info("Calling Sarvam API model=%s", self._config.model)

        response = client.chat.completions.create(
            model=self._config.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise data mapping assistant. "
                        "When asked to generate files, output ONLY the file "
                        "blocks using the exact === BEGIN/END === delimiters "
                        "specified. No reasoning, no analysis, no explanation."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            max_tokens=4096,
            extra_body={"reasoning_effort": "low"},
        )
        msg = response.choices[0].message
        # sarvam-30b separates chain-of-thought into reasoning_content; the
        # final answer is in content. Fall back to reasoning_content if content
        # is None (happens when max_tokens cuts off before the answer).
        text = msg.content
        if not text:
            raw = getattr(msg, 'reasoning_content', None)
            if raw:
                # Strip <think>…</think> wrapper if present, keep the rest
                stripped = re.sub(r'<think>.*?</think>', '', raw,
                                  flags=re.DOTALL).strip()
                text = stripped if stripped else raw
        return text or ""

    def _extract_file_content(self, response: str,
                              file_path: str) -> Optional[str]:
        """Extract content between === BEGIN <path> === and === END <path> === delimiters."""
        escaped = re.escape(file_path)
        pattern = (rf"=== BEGIN {escaped} ===\n(.*?)\n=== END {escaped} ===")
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _write_output_files(self, pvmap_content: str,
                            metadata_content: str) -> None:
        pvmap_path = Path(str(self._output_path_abs) + '_pvmap.csv')
        metadata_path = Path(str(self._output_path_abs) + '_metadata.csv')
        pvmap_path.write_text(pvmap_content, encoding='utf-8')
        metadata_path.write_text(metadata_content, encoding='utf-8')
        logging.info("Wrote pvmap: %s", pvmap_path)
        logging.info("Wrote metadata: %s", metadata_path)

    def _run_statvar_processor(self) -> int:
        """Run the statvar processor and return exit code."""
        tools_dir = os.path.abspath(os.path.join(_SCRIPT_DIR, '..'))
        script = os.path.join(_SCRIPT_DIR, 'run_statvar_processor.sh')
        cmd = [
            'bash', script,
            '--python', sys.executable,
            '--script-dir', tools_dir,
            '--working-dir', str(self._working_dir),
            '--input-data', str(self._config.data_config.input_data[0]),
            '--gemini-run-id', self._run_id,
            '--output-path', str(self._output_path_abs),
        ]
        logging.info("Running statvar processor: %s", ' '.join(cmd))
        result = subprocess.run(cmd,
                                cwd=str(self._working_dir),
                                capture_output=False)
        return result.returncode

    def _read_processor_log(self) -> str:
        log_path = self._run_dir / 'processor.log'
        if log_path.exists():
            return log_path.read_text(encoding='utf-8', errors='replace')
        return "No processor log found."

    def _read_current_pvmap(self) -> Optional[str]:
        path = Path(str(self._output_path_abs) + '_pvmap.csv')
        return path.read_text(encoding='utf-8') if path.exists() else None

    def _read_current_metadata(self) -> Optional[str]:
        path = Path(str(self._output_path_abs) + '_metadata.csv')
        return path.read_text(encoding='utf-8') if path.exists() else None

    def _get_user_confirmation(self, prompt_file: Path) -> bool:
        print("\n" + "=" * 60)
        print("PV MAP GENERATION SUMMARY (Sarvam AI)")
        print("=" * 60)
        print(f"Input data: {self._config.data_config.input_data[0]}")
        print(
            f"Dataset type: {'SDMX' if self._config.data_config.is_sdmx_dataset else 'CSV'}"
        )
        print(f"Model: {self._config.model}")
        print(f"Max iterations: {self._config.max_iterations}")
        print(f"Prompt file: {prompt_file}")
        print(f"Output path: {self._config.output_path}")
        print("=" * 60)

        while True:
            try:
                response = input(
                    "Ready to start PV map generation? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    print("PV map generation cancelled.")
                    return False
                else:
                    print("Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                print("\nCancelled.")
                return False

    def generate(self) -> GenerationResult:
        """Run the full PV map generation loop."""
        if self._config.maps_api_key:
            os.environ['MAPS_API_KEY'] = self._config.maps_api_key
        if self._config.dc_api_key:
            os.environ['DC_API_KEY'] = self._config.dc_api_key

        if not self._config.data_config.input_data:
            raise ValueError("At least one input data file required")
        if len(self._config.data_config.input_data) != 1:
            raise ValueError(
                f"Currently only single CSV file supported. "
                f"Found {len(self._config.data_config.input_data)} files.")

        api_log_path = self._run_dir / 'sarvam_api.log'

        # Generate initial prompt (no error context)
        prompt = self._render_prompt()
        prompt_file = self._run_dir / 'generate_pvmap_prompt.md'
        prompt_file.write_text(prompt, encoding='utf-8')
        logging.info("Prompt written to: %s", prompt_file)

        result = GenerationResult(run_id=self._run_id,
                                  run_dir=self._run_dir,
                                  prompt_path=prompt_file,
                                  api_log_path=api_log_path,
                                  model=self._config.model)

        if self._config.dry_run:
            logging.info("Dry run mode: prompt at %s. Skipping API call.",
                         prompt_file)
            return result

        if not self._config.skip_confirmation:
            if not self._get_user_confirmation(prompt_file):
                return result

        previous_error = None
        previous_pvmap = None
        previous_metadata = None

        for attempt in range(1, self._config.max_iterations + 1):
            logging.info("ATTEMPT %d of %d", attempt,
                         self._config.max_iterations)
            print(
                f"\nATTEMPT {attempt} of {self._config.max_iterations}: Calling Sarvam API..."
            )

            if attempt > 1:
                prompt = self._render_prompt(
                    previous_error=previous_error,
                    previous_pvmap=previous_pvmap,
                    previous_metadata=previous_metadata,
                )
                prompt_file_n = self._run_dir / f'generate_pvmap_prompt_attempt_{attempt}.md'
                prompt_file_n.write_text(prompt, encoding='utf-8')

            response = self._call_api(prompt)

            # Log raw API response
            attempt_log = self._run_dir / f'sarvam_response_attempt_{attempt}.log'
            attempt_log.write_text(response, encoding='utf-8')
            logging.info("API response saved to: %s", attempt_log)

            output_path_str = str(self._output_path_abs)
            pvmap_content = self._extract_file_content(
                response, output_path_str + '_pvmap.csv')
            metadata_content = self._extract_file_content(
                response, output_path_str + '_metadata.csv')

            if not pvmap_content or not metadata_content:
                logging.error(
                    "Could not extract pvmap.csv or metadata.csv from API response."
                )
                print("ERROR: Could not parse pvmap.csv/metadata.csv from response."
                      " Check log at %s" % attempt_log)
                if attempt < self._config.max_iterations:
                    previous_error = (
                        "The response did not contain properly formatted file content. "
                        "Make sure to use the exact delimiters:\n"
                        f"=== BEGIN {output_path_str}_pvmap.csv ===\n"
                        f"=== END {output_path_str}_pvmap.csv ===\n"
                        f"=== BEGIN {output_path_str}_metadata.csv ===\n"
                        f"=== END {output_path_str}_metadata.csv ===")
                    previous_pvmap = pvmap_content or ''
                    previous_metadata = metadata_content or ''
                    continue
                break

            self._write_output_files(pvmap_content, metadata_content)

            print(f"Running statvar processor (attempt {attempt})...")
            exit_code = self._run_statvar_processor()

            if exit_code == 0:
                output_csv = Path(str(self._output_path_abs) + '.csv')
                if output_csv.exists() and output_csv.stat().st_size > 0:
                    print(
                        f"\nSUCCESS: PV map generation completed on attempt {attempt} "
                        f"of {self._config.max_iterations}")
                    result.success = True
                    return result
                else:
                    error_msg = (
                        f"Processor succeeded (exit 0) but output file "
                        f"{output_csv} is missing or empty.")
                    logging.error(error_msg)
                    previous_error = error_msg
            else:
                previous_error = self._read_processor_log()
                logging.error("Processor failed (exit %d). Log:\n%s",
                              exit_code, previous_error[:500])

            previous_pvmap = self._read_current_pvmap() or ''
            previous_metadata = self._read_current_metadata() or ''

            if attempt < self._config.max_iterations:
                print(
                    f"ATTEMPT {attempt} FAILED - Starting attempt {attempt + 1}..."
                )
            else:
                print(
                    f"\nITERATION LIMIT REACHED: Failed after {self._config.max_iterations} attempts"
                )
                print(f"Check logs at: {self._run_dir}/")

        return result


def prepare_config() -> Config:
    data_config = DataConfig(input_data=_FLAGS.input_data or [],
                             input_metadata=_FLAGS.input_metadata or [],
                             is_sdmx_dataset=_FLAGS.sdmx_dataset)

    api_key = _FLAGS.sarvam_api_key or os.environ.get('SARVAM_API_KEY')

    return Config(
        data_config=data_config,
        dry_run=_FLAGS.dry_run,
        maps_api_key=_FLAGS.maps_api_key,
        dc_api_key=_FLAGS.dc_api_key,
        max_iterations=_FLAGS.max_iterations,
        skip_confirmation=_FLAGS.skip_confirmation,
        output_path=_FLAGS.output_path,
        working_dir=_FLAGS.working_dir,
        extra_instruction_files=_FLAGS.extra_instruction_files or [],
        extra_instruction_max_bytes=_FLAGS.extra_instruction_max_bytes,
        sarvam_api_key=api_key,
        model=_FLAGS.model,
        lite_prompt=_FLAGS.lite_prompt,
    )


def main(_):
    config = prepare_config()
    logging.info("Loaded config: %d data files, model=%s",
                 len(config.data_config.input_data), config.model)

    generator = SarvamPVMapGenerator(config)
    result = generator.generate()

    if result.success:
        logging.info("PV Map generation succeeded.")
    else:
        logging.warning("PV Map generation did not succeed. Check: %s",
                        result.run_dir)
    return 0


if __name__ == '__main__':
    _define_flags()
    app.run(main)
