#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")"

# List of required Python libraries
libs=("flask" "psutil" "humanize" "py-cpuinfo" "gputil")
libspre=("flask" "psutil" "humanize" "cpuinfo" "gputil")

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python first."
    exit 1
fi

# Check and install required Python libraries
for lib in "${libspre[@]}"; do
    python3 -c "import $lib" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Installing $lib..."
        pip3 install "$lib"
        if [ $? -ne 0 ]; then
            echo "Failed to install $lib. Please check your internet connection and try again."
            exit 1
        fi
    else
        echo "$lib is already installed. Skipping..."
    fi
done

# Run the server
echo "==========================================="
echo "running server..."
echo "==========================================="
python3 app.py
exit 0
