#!/bin/bash
# Dataset: CDC Social Vulnerability Index
# Description: Run Claude agentic import workflow on CDC health/social data

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATASET_NAME="cdc_svi"
SOURCE_DIR="$ROOT_DIR/statvar_imports/cdc/social_vulnerability_index"
OUTPUT_DIR="$ROOT_DIR/test_import_example/$DATASET_NAME"

echo "=========================================="
echo "Running Claude Import: CDC Social Vulnerability Index"
echo "=========================================="
echo "Source: $SOURCE_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Step 1: Create output directory structure
echo "[1/6] Creating directories..."
mkdir -p "$OUTPUT_DIR/input"
mkdir -p "$OUTPUT_DIR/output_claude"
mkdir -p "$OUTPUT_DIR/final_output"

# Step 2: Copy input files and ground truth
echo "[2/6] Copying input and ground truth files..."
cp "$SOURCE_DIR/test_data/SVI_2022_US_county_input.csv" "$OUTPUT_DIR/input/"
cp "$SOURCE_DIR/pvmap.csv" "$OUTPUT_DIR/input/expected_pvmap.csv"
cp "$SOURCE_DIR/test_data/SVI_2022_US_county.csv" "$OUTPUT_DIR/input/expected_output.csv"
cp "$SOURCE_DIR/test_data/SVI_2022_US_county.tmcf" "$OUTPUT_DIR/input/expected_output.tmcf"

# Step 3: Activate Python environment
echo "[3/6] Activating Python environment..."
cd "$ROOT_DIR"
source .env/bin/activate

# Step 4: Run Claude PV Map generation
echo "[4/6] Running Claude PV Map generation..."
cd "$OUTPUT_DIR"
python "$ROOT_DIR/tools/agentic_import/pvmap_generator.py" \
  --input_data="input/SVI_2022_US_county_input.csv" \
  --output_path="output_claude/output" \
  --llm_cli="claude" \
  --skip_confirmation

# Step 5: Process full dataset with generated PV map
echo "[5/6] Processing dataset with generated PV map..."
python "$ROOT_DIR/tools/statvar_importer/stat_var_processor.py" \
  --input_data="input/SVI_2022_US_county_input.csv" \
  --pv_map="output_claude/output_pvmap.csv" \
  --config_file="output_claude/output_metadata.csv" \
  --generate_statvar_name=True \
  --output_path="final_output/output"

# Step 6: Report results
echo ""
echo "=========================================="
echo "[6/6] Results: CDC Social Vulnerability Index"
echo "=========================================="
echo "Claude PV Map:     $OUTPUT_DIR/output_claude/output_pvmap.csv"
echo "Claude Output:     $OUTPUT_DIR/final_output/output.csv"
echo "Expected Output:   $OUTPUT_DIR/input/expected_output.csv"
echo ""
echo "To compare outputs:"
echo "  diff $OUTPUT_DIR/final_output/output.csv $OUTPUT_DIR/input/expected_output.csv"
echo ""
echo "Done!"
