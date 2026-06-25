#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting installation of RFID CLI Manager...${NC}"

# 1. Update system and install basic dependencies
echo -e "${GREEN}Updating system and installing dependencies...${NC}"
sudo apt update && sudo apt install -y python3-pip git i2c-tools

# 2. Install necessary Python libraries
# Using --break-system-packages for newer Raspberry Pi OS versions (Bookworm+)
echo -e "${GREEN}Installing Python requirements...${NC}"
pip3 install py532lib --break-system-packages

# 3. Enable I2C interface
echo -e "${GREEN}Ensuring I2C is enabled...${NC}"
sudo raspi-config nonint do_i2c 0

# 4. Git configuration (to support the update function)
echo -e "${GREEN}Setting up Git repository...${NC}"
if [ ! -d ".git" ]; then
    echo "This folder is not a git repository. Please ensure you are inside the cloned project directory."
else
    # Configure git to pull without rebase conflicts
    git config pull.rebase false
fi

echo -e "${BLUE}Installation complete!${NC}"
echo -e "You can now run the app with: ${GREEN}python3 main.py${NC}"