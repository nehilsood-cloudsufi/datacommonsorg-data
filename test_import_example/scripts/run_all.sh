#!/bin/bash
# Run all 5 dataset import scripts in sequence
# Description: Execute Claude agentic import workflow on all test datasets

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "Running Claude Import on ALL 5 Test Datasets"
echo "============================================================"
echo ""
echo "Datasets to process:"
echo "  1. BIS Central Bank Policy Rate"
echo "  2. Census SAIPE"
echo "  3. CDC Social Vulnerability Index"
echo "  4. India NSS Health Ailments"
echo "  5. Zurich Population"
echo ""
echo "============================================================"

# Track results
BIS_RESULT="NOT_RUN"
SAIPE_RESULT="NOT_RUN"
CDC_SVI_RESULT="NOT_RUN"
INDIA_NSS_RESULT="NOT_RUN"
ZURICH_RESULT="NOT_RUN"

# Run each script
echo ""
echo "[1/5] Running BIS Central Bank Policy Rate..."
echo "------------------------------------------------------------"
if "$SCRIPT_DIR/run_bis.sh"; then
    BIS_RESULT="SUCCESS"
else
    BIS_RESULT="FAILED"
fi

echo ""
echo "[2/5] Running Census SAIPE..."
echo "------------------------------------------------------------"
if "$SCRIPT_DIR/run_saipe.sh"; then
    SAIPE_RESULT="SUCCESS"
else
    SAIPE_RESULT="FAILED"
fi

echo ""
echo "[3/5] Running CDC Social Vulnerability Index..."
echo "------------------------------------------------------------"
if "$SCRIPT_DIR/run_cdc_svi.sh"; then
    CDC_SVI_RESULT="SUCCESS"
else
    CDC_SVI_RESULT="FAILED"
fi

echo ""
echo "[4/5] Running India NSS Health Ailments..."
echo "------------------------------------------------------------"
if "$SCRIPT_DIR/run_india_nss.sh"; then
    INDIA_NSS_RESULT="SUCCESS"
else
    INDIA_NSS_RESULT="FAILED"
fi

echo ""
echo "[5/5] Running Zurich Population..."
echo "------------------------------------------------------------"
if "$SCRIPT_DIR/run_zurich.sh"; then
    ZURICH_RESULT="SUCCESS"
else
    ZURICH_RESULT="FAILED"
fi

# Print summary
echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo ""
echo "| Dataset                  | Status  |"
echo "|--------------------------|---------|"
echo "| BIS Central Bank Policy  | $BIS_RESULT |"
echo "| Census SAIPE             | $SAIPE_RESULT |"
echo "| CDC Social Vulnerability | $CDC_SVI_RESULT |"
echo "| India NSS Health         | $INDIA_NSS_RESULT |"
echo "| Zurich Population        | $ZURICH_RESULT |"
echo ""
echo "============================================================"
echo "All datasets processed!"
echo ""
echo "Results saved in:"
echo "  - test_import_example/bis/"
echo "  - test_import_example/saipe/"
echo "  - test_import_example/cdc_svi/"
echo "  - test_import_example/india_nss/"
echo "  - test_import_example/zurich/"
echo ""
