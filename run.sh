#!/bin/bash

# Calendar and Reminder App - Setup and Launch Script for Unix/Linux/macOS

echo ""
echo "============================================================"
echo "    Calendar and Reminder App - Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Display Python version
python3 --version

echo ""
echo "Installing dependencies..."
echo ""

# Install requirements
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "Warning: Some dependencies may have failed to install"
    echo "Attempting minimal installation..."
    pip3 install customtkinter pillow tkcalendar playsound
fi

echo ""
echo "Setup complete!"
echo "Launching Calendar and Reminder App..."
echo ""

# Launch the application
python3 main.py
