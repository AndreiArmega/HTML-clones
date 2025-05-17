#!/bin/bash

set -euo pipefail

echo "Creating virtual environment in ./venv"
python3 -m venv venv

source venv/bin/activate
echo "Virtual environment activated."

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python packages..."
pip install \
  imagehash==4.3.2 \
  numpy==2.2.5 \
  Pillow==11.2.1 \
  playwright==1.52.0 \
  skimage==0.0 \
  torch==2.7.0 \
  torchvision==0.22.0 \
  tqdm==4.67.1

echo "Installing Playwright browsers (if used)..."
playwright install

echo "All packages installed successfully."

