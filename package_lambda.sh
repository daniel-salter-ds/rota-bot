#!/bin/bash

# Configuration
REQUIREMENTS_FILE="requirements.txt"
PACKAGE_DIR="package"
ZIP_FILE="lambda_function.zip"
LAMBDA_FUNCTION="lambda_function.py"

# Step 1: Install dependencies into the package directory
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE" --target "$PACKAGE_DIR"
else
    echo "No $REQUIREMENTS_FILE found, skipping dependency installation."
fi

# Step 2: Navigate to the package directory and zip the dependencies
if [ -d "$PACKAGE_DIR" ]; then
    echo "Zipping dependencies from $PACKAGE_DIR..."
    cd "$PACKAGE_DIR" || exit
    zip -r9 "../$ZIP_FILE" .
    cd ..
else
    echo "Error: $PACKAGE_DIR directory does not exist."
    exit 1
fi

# Step 3: Add the Lambda function handler to the zip
if [ -f "$LAMBDA_FUNCTION" ]; then
    echo "Adding $LAMBDA_FUNCTION to the zip file..."
    zip -g "$ZIP_FILE" "$LAMBDA_FUNCTION"
else
    echo "Error: $LAMBDA_FUNCTION file does not exist."
    exit 1
fi

echo "Packaging complete: $ZIP_FILE"
