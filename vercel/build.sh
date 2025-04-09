#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Starting build process..."

# Install system dependencies (required for geopandas)
apt-get update && apt-get install -y \
    libgdal-dev \
    python3-dev \
    python3-pip

# Create and activate virtual environment (Vercel uses Python 3.9 by default)
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If you need any data processing steps, add them here
# For example:
# python scripts/process_data.py

echo "Build completed successfully!"
