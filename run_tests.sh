#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Activating virtual environment..."

# Activate venv
source .venv/bin/activate

echo "Running test suite..."

# Run pytest
pytest

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Tests failed."
    exit 1
fi