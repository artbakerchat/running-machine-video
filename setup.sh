#!/bin/bash

# Running Machine Video Sync - Quick Start Script
# This script automates the setup and launch process

set -e

echo "================================"
echo "Running Machine Video Sync"
echo "Quick Start Setup"
echo "================================"
echo ""

# Check Python installation
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ Found $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create video directory
echo "[5/5] Setting up directories..."
mkdir -p static/videos
echo "✓ Directories created"
echo ""

echo "================================"
echo "Setup Complete! ✓"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Add your running video to: static/videos/running.mp4"
echo "2. Start the server: python app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "Or run the sensor simulator:"
echo "   python sensor_simulator.py"
echo ""
echo "To deactivate virtual environment: deactivate"
