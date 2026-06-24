#!/bin/bash

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
#
# PV Map generator using Sarvam AI API.
# Usage:
#   export SARVAM_API_KEY="your-api-key"
#   ./generate_pvmap_sarvam.sh \
#       --input_data=sample_data.csv \
#       --model=sarvam-m \
#       --output_path=output/output

set -euo pipefail

ORIGINAL_DIR="$(pwd)"
SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
DATA_REPO_ROOT="$(realpath "$SCRIPT_DIR/../..")"

echo "Current/Original directory: $ORIGINAL_DIR"
echo "Script directory: $SCRIPT_DIR"
echo "Data repository root: $DATA_REPO_ROOT"

function validate_requirements {
    # Check for Sarvam API key
    if [ -z "${SARVAM_API_KEY:-}" ]; then
        # Allow --sarvam_api_key flag to pass it in too
        if ! echo "$@" | grep -q "sarvam_api_key"; then
            echo "Warning: SARVAM_API_KEY environment variable not set."
            echo "Set it with: export SARVAM_API_KEY='your-api-key'"
            echo "Or pass --sarvam_api_key=YOUR_KEY as an argument."
        fi
    fi

    # Check for openai Python package
    if ! python3 -c "import openai" 2>/dev/null; then
        echo "Error: openai Python package not installed."
        echo "Install with: pip install openai"
        exit 1
    fi
}

function setup_python_environment {
    cd "$DATA_REPO_ROOT"
    if [ "${SKIP_PYTHON_SETUP:-}" != "true" ]; then
        echo "Setting up Python environment..."
        ./run_tests.sh -r
    else
        echo "Skipping Python environment setup (SKIP_PYTHON_SETUP=true)"
    fi
    echo "Activating Python virtual environment..."
    source .venv/bin/activate
}

function run_sarvam_pvmap_generator {
    cd "$ORIGINAL_DIR"
    echo "Running Sarvam PV Map generator from: $(pwd)"
    python3 "$SCRIPT_DIR/sarvam_pvmap_generator.py" "$@"
}

validate_requirements "$@"
setup_python_environment
mkdir -p "$ORIGINAL_DIR/.datacommons"
run_sarvam_pvmap_generator "$@"
echo "PV Map generation completed."
