#!/bin/bash

# Configuration
REQUIREMENTS_FILE="requirements.txt"
PACKAGE_DIR="package"
ZIP_FILE="lambda_function.zip"
LAMBDA_FUNCTION="lambda_function.py"
LOCAL_DEPENDENCIES=("sheet.py" "model/")  # Local files and directories
AWS_LAMBDA_FUNCTION_NAME="sendRotaReminder"
ENV_FILE=".env"


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

# Step 3: Add the Lambda function handler and additional local dependencies to the zip
if [ -f "$LAMBDA_FUNCTION" ]; then
    echo "Adding $LAMBDA_FUNCTION to the zip file..."
    zip -g "$ZIP_FILE" "$LAMBDA_FUNCTION"
else
    echo "Error: $LAMBDA_FUNCTION file does not exist."
    exit 1
fi

# Step 4: Add additional local dependencies (utils.py, config/) to the zip
for item in "${LOCAL_DEPENDENCIES[@]}"; do
    if [ -f "$item" ]; then
        echo "Adding $item to the zip file..."
        zip -g "$ZIP_FILE" "$item"
    elif [ -d "$item" ]; then
        echo "Adding directory $item to the zip file..."
        zip -r9 "$ZIP_FILE" "$item"
    else
        echo "Error: $item does not exist."
        exit 1
    fi
done

echo "Packaging complete: $ZIP_FILE"

# Step 5: Parse the .env file and format it for environment variables
if [ -f "$ENV_FILE" ]; then
    echo "Parsing $ENV_FILE..."

    # Read the .env file and convert it into the required format
    env_vars=$(grep -v '^#' "$ENV_FILE" | sed 's/^export //g' | awk -F= '{print $1 "=" $2}' | tr '\n' ',' | sed 's/,$//')

    # Update the Lambda function environment variables
    echo "Updating environment variables from $ENV_FILE..."

    aws lambda update-function-configuration \
        --profile rota-bot \
        --function-name "$AWS_LAMBDA_FUNCTION_NAME" \
        --environment "Variables={$env_vars}" \
        --no-cli-pager

    if [ $? -eq 0 ]; then
        echo "Environment variables updated successfully."
    else
        echo "Failed to update environment variables."
        exit 1
    fi
else
    echo "No $ENV_FILE found, skipping environment variable update."
fi

# Step 6: Upload the zip file to AWS Lambda
echo "Uploading $ZIP_FILE to AWS Lambda function '$AWS_LAMBDA_FUNCTION_NAME'..."

aws lambda update-function-code \
    --profile rota-bot \
    --function-name "$AWS_LAMBDA_FUNCTION_NAME" \
    --zip-file fileb://"$ZIP_FILE" \
    --publish \
    --no-cli-pager

if [ $? -eq 0 ]; then
    echo "Lambda function '$AWS_LAMBDA_FUNCTION_NAME' updated successfully."
else
    echo "Failed to update Lambda function."
    exit 1
fi