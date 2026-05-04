# How to Use the Agentic Import Tool

The Agentic Import Tool automates the process of importing CSV/SDMX data into Google's Data Commons platform using AI (Gemini CLI) to generate Property-Value (PV) mappings.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Workflow](#step-by-step-workflow)
3. [Command Line Flags Reference](#command-line-flags-reference)
4. [Debugging Tips](#debugging-tips)
5. [Real-World Examples](#real-world-examples)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Install Gemini CLI

The tool requires Google's Gemini CLI to be installed and accessible in your PATH.

```bash
# Install Gemini CLI - follow the official guide:
# https://github.com/google-gemini/gemini-cli

# Verify installation
which gemini
gemini --version
```

### 2. Get Data Commons API Key (Optional but Recommended)

The API key enables place resolution and validation against the Data Commons knowledge graph.

```bash
# Get your API key from:
# https://docs.datacommons.org/api/#obtain-an-api-key

# Set as environment variable
export DC_API_KEY="your_data_commons_api_key_here"
```

### 3. Setup Python Environment

```bash
# Clone the Data Commons data repository (if not already done)
git clone https://github.com/datacommonsorg/data.git
cd data

# Set repository path environment variable
export DC_DATA_REPO_PATH="$(pwd)"

# Setup Python virtual environment
./run_tests.sh -r

# Activate the environment
source .env/bin/activate

# Verify Python environment
python --version  # Should be Python 3.x
```

---

## Step-by-Step Workflow

### Step 1: Prepare Your Working Directory

Create a dedicated working directory for your import project.

```bash
# Create a working directory
mkdir -p /path/to/my_import
cd /path/to/my_import

# Your directory should contain:
# - input_data.csv        (required: your source data)
# - metadata files        (optional: JSON, XML, YAML, TXT files with context)
```

**Example directory structure:**
```
my_import/
├── input_data.csv           # Your raw CSV data
├── data_dictionary.json     # Optional: metadata describing columns
└── source_info.txt          # Optional: information about the data source
```

### Step 2: Sample Your Data

The tool works best with a sample of your data (default: 30 rows). This keeps Gemini's context efficient and reduces processing time.

```bash
python $DC_DATA_REPO_PATH/tools/statvar_importer/data_sampler.py \
  --sampler_input="input_data.csv" \
  --sampler_output="sample_data.csv" \
  --sampler_output_rows=30
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--sampler_input` | Path to your full CSV file | Required |
| `--sampler_output` | Path for the sample output | Required |
| `--sampler_output_rows` | Number of rows to sample | 30 |

> **Tip:** For non-SDMX sources, set `--sampler_output_rows` large enough to capture all unique values in categorical columns.

### Step 3: Extract SDMX Metadata (If Applicable)

Only needed if your data source is in SDMX format:

```bash
python $DC_DATA_REPO_PATH/tools/agentic_import/sdmx_metadata_extractor.py \
  --input_metadata="metadata.xml" \
  --output_path="sdmx_metadata.json"
```

This converts complex SDMX XML structures into a token-efficient JSON format that Gemini can process effectively.

### Step 4: Generate PV Map Using Gemini AI

This is the core step where AI generates the property-value mappings.

**For Standard CSV Data:**

```bash
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample_data.csv" \
  --input_metadata="metadata.json" \
  --output_path="output/output"
```

**For SDMX Data:**

```bash
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample_data.csv" \
  --input_metadata="sdmx_metadata.json" \
  --output_path="output/output" \
  --sdmx_dataset
```

**What Happens During Execution:**

1. Tool creates `.datacommons/runs/gemini_YYYYMMDD_HHMMSS/` directory
2. Generates a comprehensive prompt from Jinja2 templates
3. Shows you a summary and asks for confirmation (unless `--skip_confirmation`)
4. Pipes the prompt to Gemini CLI
5. Gemini analyzes data and generates `pvmap.csv` and `metadata.csv`
6. Gemini calls the StatVar processor to validate
7. If validation fails, Gemini retries (up to `--max_iterations`)

**Generated Files:**

```
output/
├── output_pvmap.csv           # Column-to-property mappings
├── output_metadata.csv        # Processor configuration
├── output.csv                 # Sample data in Data Commons format
├── output.tmcf                # Template MCF file
└── output_stat_vars.mcf       # StatVar definitions
```

### Step 5: Process Full Dataset

Once the sample validates successfully, process your complete data:

```bash
python $DC_DATA_REPO_PATH/tools/statvar_importer/stat_var_processor.py \
  --input_data="input_data.csv" \
  --pv_map="output/output_pvmap.csv" \
  --config_file="output/output_metadata.csv" \
  --generate_statvar_name=True \
  --skip_constant_csv_columns=False \
  --output_path="final_output/output"
```

**Output Files:**

```
final_output/
├── output.csv                 # Full dataset as Data Commons observations
├── output.tmcf                # Template MCF
├── output_stat_vars.mcf       # StatVar definitions
└── output_stat_vars_schema.mcf # Schema file (optional)
```

### Step 6: (Optional) Generate Custom DC Config

For custom Data Commons instances:

```bash
python $DC_DATA_REPO_PATH/tools/agentic_import/generate_custom_dc_config.py \
  --input_csv="final_output/output.csv" \
  --output_config="final_output/config.json"
```

---

## Command Line Flags Reference

### pvmap_generator.py Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input_data` | list | **Required** | CSV file(s) to process. Currently supports single file only. |
| `--input_metadata` | list | `[]` | Metadata files (JSON, XML, YAML, TXT). Comma-separated. |
| `--sdmx_dataset` | bool | `False` | Enable SDMX-specific processing and knowledge base. |
| `--output_path` | string | `output/output` | Output directory and filename prefix. |
| `--dry_run` | bool | `False` | Generate prompt only, don't execute Gemini. |
| `--skip_confirmation` | bool | `False` | Skip the y/n confirmation prompt. |
| `--enable_sandboxing` | bool | `True` (macOS) | Run Gemini in sandboxed mode. |
| `--max_iterations` | int | `10` | Maximum retry attempts for StatVar processor. |
| `--dc_api_key` | string | `None` | Data Commons API key for place resolution. |
| `--maps_api_key` | string | `None` | Google Maps API key for geocoding. |
| `--gemini_cli` | string | `gemini` | Custom path to Gemini CLI executable. |

### stat_var_processor.py Key Flags

| Flag | Description |
|------|-------------|
| `--input_data` | Input CSV file path |
| `--pv_map` | Path to property-value mapping CSV |
| `--config_file` | Path to metadata configuration CSV |
| `--output_path` | Output file prefix |
| `--generate_statvar_name` | Auto-generate StatVar names from properties |
| `--skip_constant_csv_columns` | Omit columns with constant values from CSV |
| `--output_columns` | Order of columns in output CSV |

### data_sampler.py Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--sampler_input` | Path to input CSV file | Required |
| `--sampler_output` | Path for sampled output CSV | Required |
| `--sampler_output_rows` | Number of rows to include in sample | 30 |

---

## Debugging Tips

### 1. Check Gemini CLI Logs

All Gemini interactions are logged for debugging:

```bash
# List all runs
ls -la .datacommons/runs/

# View the most recent run's log
cat .datacommons/runs/gemini_*/gemini_cli.log

# View a specific run
cat .datacommons/runs/gemini_20250108_143022/gemini_cli.log
```

### 2. Examine the Generated Prompt

See exactly what was sent to Gemini:

```bash
cat .datacommons/runs/gemini_*/generate_pvmap_prompt.md
```

### 3. Review Processor Logs

If the StatVar processor fails:

```bash
# Main processor log
cat .datacommons/processor.log

# Per-attempt logs
cat .datacommons/runs/gemini_*/attempt_001/processor.log
cat .datacommons/runs/gemini_*/attempt_002/processor.log
```

### 4. Inspect Backup Manifests

See what was backed up for each attempt:

```bash
cat .datacommons/runs/gemini_*/attempt_*/backup_manifest.txt
```

### 5. Use Dry Run Mode

Test prompt generation without executing Gemini:

```bash
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample_data.csv" \
  --output_path="output/output" \
  --dry_run
```

Then inspect the generated prompt:

```bash
cat .datacommons/runs/gemini_*/generate_pvmap_prompt.md
```

### 6. Directory Structure After a Run

Understanding the output structure helps with debugging:

```
my_import/
├── input_data.csv                 # Your original data
├── sample_data.csv                # Sampled data (30 rows)
├── output/                        # Generated outputs
│   ├── output_pvmap.csv
│   ├── output_metadata.csv
│   ├── output.csv
│   ├── output.tmcf
│   └── output_stat_vars.mcf
├── final_output/                  # Full processed data
│   └── ...
└── .datacommons/                  # Logs and backups
    ├── processor.log              # Latest processor log
    ├── backup.log                 # Backup log
    └── runs/
        └── gemini_20250108_143022/
            ├── generate_pvmap_prompt.md   # Prompt sent to Gemini
            ├── gemini_cli.log             # Full Gemini output
            ├── attempt_001/               # First attempt
            │   ├── backup_manifest.txt
            │   ├── processor.log
            │   ├── output_pvmap.csv
            │   └── output.csv
            └── attempt_002/               # Retry (if needed)
```

---

## Real-World Examples

### Example 1: US Urban School Data

```bash
# 1. Navigate to the import directory
cd $DC_DATA_REPO_PATH/statvar_imports/us_urban_school/

# 2. Download the data (if needed)
python3 download_statelevel.py --data_type=sat_act

# 3. Sample the data
python $DC_DATA_REPO_PATH/tools/statvar_importer/data_sampler.py \
  --sampler_input="2022_SAT_ACT_Participation.csv" \
  --sampler_output="sample.csv" \
  --sampler_output_rows=30

# 4. Generate PV map with AI
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --output_path="output/output"

# 5. Review the generated files
cat output/output_pvmap.csv
cat output/output_metadata.csv

# 6. Process full dataset
python $DC_DATA_REPO_PATH/tools/statvar_importer/stat_var_processor.py \
  --input_data="2022_SAT_ACT_Participation.csv" \
  --pv_map="output/output_pvmap.csv" \
  --config_file="output/output_metadata.csv" \
  --generate_statvar_name=True \
  --output_path="final/output"

# 7. Verify outputs
head final/output.csv
cat final/output_stat_vars.mcf
```

### Example 2: SDMX Data (BIS Central Bank Policy Rates)

```bash
# 1. Create working directory
mkdir bis_import && cd bis_import

# 2. Extract SDMX metadata
python $DC_DATA_REPO_PATH/tools/agentic_import/sdmx_metadata_extractor.py \
  --input_metadata="bis_cbpol_structure.xml" \
  --output_path="sdmx_metadata.json"

# 3. Sample the data
python $DC_DATA_REPO_PATH/tools/statvar_importer/data_sampler.py \
  --sampler_input="bis_cbpol_data.csv" \
  --sampler_output="sample.csv" \
  --sampler_output_rows=50

# 4. Generate PV map with SDMX mode
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --input_metadata="sdmx_metadata.json" \
  --output_path="output/output" \
  --sdmx_dataset

# 5. Process full dataset
python $DC_DATA_REPO_PATH/tools/statvar_importer/stat_var_processor.py \
  --input_data="bis_cbpol_data.csv" \
  --pv_map="output/output_pvmap.csv" \
  --config_file="output/output_metadata.csv" \
  --generate_statvar_name=True \
  --output_path="final/output"
```

### Example 3: Quick Test with Dry Run

```bash
# Generate prompt without running Gemini (for testing/review)
python $DC_DATA_REPO_PATH/tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --output_path="output/output" \
  --dry_run

# Review the generated prompt
cat .datacommons/runs/gemini_*/generate_pvmap_prompt.md | head -100
```

---

## Troubleshooting

### Common Issues and Solutions

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| "Gemini CLI not found" | Gemini not in PATH | Install Gemini CLI or use `--gemini_cli=/path/to/gemini` |
| "Path outside working directory" | Security validation failed | Ensure all input files are within your working directory |
| "No data in output" | Wrong `header_rows` in metadata.csv | Check that `header_rows` is set correctly (usually `1` for standard CSV) |
| "Wrong place resolution" | Ambiguous place names | Add `place_type` and `places_within` to metadata.csv |
| Infinite retry loop | Persistent validation errors | Check `.datacommons/processor.log` for specific errors |
| Empty StatVars | Missing mandatory properties | Ensure `populationType`, `measuredProperty`, `statType` are mapped |
| "Currently only single CSV file is supported" | Multiple files passed | Pass only one CSV file to `--input_data` |

### Metadata.csv Common Mistakes

1. **Missing `header_rows`**: Most CSV files have headers, but `header_rows` defaults to 0. Always set to `1` for standard CSV files.

2. **Using CLI flag names**: Use parameter names like `header_rows`, not CLI flag names like `--header_rows`.

3. **Forgetting `places_within`**: Geographic data without this constraint can resolve to wrong places (e.g., Paris, Texas instead of Paris, France).

### Getting Help

- Check the [README.md](README.md) for additional documentation
- Review the generated prompt at `.datacommons/runs/gemini_*/generate_pvmap_prompt.md`
- Examine processor logs at `.datacommons/processor.log`

---

## Quick Reference

### Minimum Viable Command (Standard CSV)

```bash
# 1. Sample
python tools/statvar_importer/data_sampler.py \
  --sampler_input="data.csv" \
  --sampler_output="sample.csv"

# 2. Generate PV map
python tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --output_path="output/output"

# 3. Process full data
python tools/statvar_importer/stat_var_processor.py \
  --input_data="data.csv" \
  --pv_map="output/output_pvmap.csv" \
  --config_file="output/output_metadata.csv" \
  --output_path="final/output"
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DC_API_KEY` | Data Commons API key for place resolution |
| `MAPS_API_KEY` | Google Maps API key for geocoding |
| `DC_DATA_REPO_PATH` | Path to the datacommonsorg/data repository |
