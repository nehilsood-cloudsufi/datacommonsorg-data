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
# Starts a LiteLLM proxy that intercepts Gemini CLI API calls and routes them
# to Sarvam AI. This lets generate_pvmap.sh run unchanged while using Sarvam.
#
# Usage:
#   export SARVAM_API_KEY="your-sarvam-api-key"
#   ./start_sarvam_proxy.sh            # starts proxy on port 4000 (default)
#   ./start_sarvam_proxy.sh --port 4001 --model sarvam-l
#
# After this script prints "Proxy ready", open a new terminal and run:
#   source <(./start_sarvam_proxy.sh --print-env)
#   ./generate_pvmap.sh --input_data=... (unchanged)

set -euo pipefail

SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
PORT=4000
MODEL="sarvam-30b"
PRINT_ENV=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --port)
      PORT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --print-env)
      PRINT_ENV=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--port PORT] [--model sarvam-m|sarvam-l] [--print-env]"
      exit 1
      ;;
  esac
done

# If --print-env flag, just output the export commands and exit (for sourcing)
if [ "$PRINT_ENV" = "true" ]; then
  echo "export GOOGLE_GEMINI_BASE_URL=\"http://localhost:${PORT}\""
  echo "export GEMINI_API_KEY=\"dummy-key-litellm-handles-auth\""
  exit 0
fi

# Validate API key
if [ -z "${SARVAM_API_KEY:-}" ]; then
  echo "Error: SARVAM_API_KEY environment variable not set."
  echo "Set it with: export SARVAM_API_KEY='your-api-key'"
  exit 1
fi

# Check LiteLLM installation
if ! command -v litellm &> /dev/null; then
  echo "LiteLLM not found. Installing..."
  pip install "litellm[proxy]" -q
fi

# Write a temporary config with the chosen model substituted in
TEMP_CONFIG="$(mktemp /tmp/litellm_sarvam_XXXXXX.yaml)"

# Patch the model name in the config: replace all 'openai/sarvam-m' with the chosen model
sed "s|openai/sarvam-m|openai/${MODEL}|g" \
  "$SCRIPT_DIR/litellm_sarvam_config.yaml" > "$TEMP_CONFIG"

# Store PID file so we can stop it later
PID_FILE="/tmp/litellm_sarvam_proxy.pid"

echo "========================================"
echo "Starting LiteLLM Sarvam Proxy"
echo "  Port  : ${PORT}"
echo "  Model : ${MODEL} (via Sarvam AI)"
echo "  Config: ${TEMP_CONFIG}"
echo "========================================"

# Start proxy in background
litellm --config "$TEMP_CONFIG" --port "$PORT" &
PROXY_PID=$!
echo "$PROXY_PID" > "$PID_FILE"

echo "Proxy PID: ${PROXY_PID} (saved to ${PID_FILE})"
echo "Stop proxy with: kill \$(cat ${PID_FILE})"
echo ""

# Wait for proxy to become healthy
echo "Waiting for proxy to be ready..."
for i in $(seq 1 30); do
  if curl -s "http://localhost:${PORT}/health" > /dev/null 2>&1; then
    echo "Proxy is ready!"
    break
  fi
  sleep 1
  if ! kill -0 "$PROXY_PID" 2>/dev/null; then
    echo "Error: Proxy process died. Check logs above."
    rm -f "$TEMP_CONFIG"
    exit 1
  fi
done

echo ""
echo "========================================"
echo "Proxy ready at: http://localhost:${PORT}"
echo ""
echo "In your agentic_import terminal, run:"
echo "  export GOOGLE_GEMINI_BASE_URL=\"http://localhost:${PORT}\""
echo "  export GEMINI_API_KEY=\"dummy-key-litellm-handles-auth\""
echo ""
echo "Or source these automatically:"
echo "  source <($SCRIPT_DIR/start_sarvam_proxy.sh --print-env --port ${PORT})"
echo ""
echo "Then run generate_pvmap.sh as normal:"
echo "  ./generate_pvmap.sh --input_data=sample.csv --output_path=output/output"
echo "========================================"

# Keep process alive (the litellm proxy is in background)
wait "$PROXY_PID"

# Cleanup temp config on exit
rm -f "$TEMP_CONFIG"
