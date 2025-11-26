#!/bin/bash
# Setup script for CD Exercise
# Run this script to set up your local development environment

set -e

echo "=== CD Exercise Setup ==="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "ERROR: pip is not installed"
    exit 1
fi
echo "✓ pip found"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "WARNING: Docker is not installed. You'll need it for later exercises."
else
    echo "✓ Docker found: $(docker --version)"
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    exit 1
fi
echo "✓ Git found: $(git --version)"

echo ""
echo "Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip > /dev/null
echo "✓ pip upgraded"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements-dev.txt > /dev/null
echo "✓ Dependencies installed"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To run the application locally:"
echo "  python -m src.app.main"
echo ""
echo "To build with Docker:"
echo "  docker build -t cd-exercise ."
echo ""
echo "Happy learning!"
