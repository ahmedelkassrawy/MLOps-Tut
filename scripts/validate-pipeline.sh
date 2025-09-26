#!/bin/bash

# DVC Pipeline Validation Script for CI/CD

set -e  # Exit on any error

echo "🔍 Validating DVC Pipeline..."

# Check if required files exist
echo "📁 Checking required files..."
required_files=("dvc.yaml" "params.yaml" "requirements.txt" "src/data_collection.py" "src/data_prep.py" "src/model_building.py" "src/model_eval.py")

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Missing required file: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done

# Validate DVC pipeline structure
echo "🔧 Validating DVC pipeline structure..."
timeout 10 dvc dag >/dev/null 2>&1 || { 
    echo "❌ DVC pipeline validation failed - checking alternative method..."
    # Try alternative validation using dvc status
    dvc status >/dev/null 2>&1 || { echo "❌ DVC pipeline validation failed"; exit 1; }
}
echo "✅ DVC pipeline structure is valid"

# Check if Python dependencies can be installed
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run DVC pipeline (dry run first)
echo "🧪 Testing DVC pipeline (dry run)..."
dvc repro --dry > /dev/null 2>&1 || { echo "❌ DVC dry run failed"; exit 1; }
echo "✅ DVC dry run successful"

# Run actual DVC pipeline
echo "🚀 Running DVC pipeline..."
dvc repro

# Verify model file was created
if [[ ! -f "model.pkl" ]]; then
    echo "❌ Model file (model.pkl) was not generated"
    exit 1
else
    echo "✅ Model file generated successfully"
fi

# Verify metrics file was created
if [[ ! -f "metrics.json" ]]; then
    echo "❌ Metrics file (metrics.json) was not generated"
    exit 1
else
    echo "✅ Metrics file generated successfully"
fi

echo "🎉 All validations passed! Pipeline is ready for Docker build."