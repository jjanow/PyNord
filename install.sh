#!/bin/bash

# PyNord Installation Script
# This script installs PyNord and its dependencies on Kubuntu/Linux

set -e

echo "=== PyNord - NordVPN Management Application ==="
echo "Installing PyNord and dependencies..."
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "Python version: $python_version ✓"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-venv python3-dev build-essential

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv pynord_env
source pynord_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install PyNord
echo "Installing PyNord..."
pip install -e .

echo
echo "=== Installation Complete! ==="
echo
echo "To run PyNord:"
echo "1. Activate the virtual environment: source pynord_env/bin/activate"
echo "2. Run the application: python main.py"
echo
echo "Or create a desktop shortcut:"
echo "1. Create a .desktop file in ~/.local/share/applications/"
echo "2. Point it to: $(pwd)/pynord_env/bin/python $(pwd)/main.py"
echo
echo "Note: Make sure NordVPN CLI is installed and configured before using PyNord."
echo "See README.md for NordVPN CLI installation instructions." 