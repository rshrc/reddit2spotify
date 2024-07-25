#!/bin/bash

# Define variables
PROJECT_DIR=$(pwd)
SCRIPT_NAME="run_reddit_to_spotify.sh"
ALIAS_NAME="musicpls"
SHELL_RC=""

# Detect the user's shell and set the configuration file accordingly
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "Unsupported shell. Please use bash or zsh."
    exit 1
fi

echo "#!/bin/bash
cd $PROJECT_DIR
poetry run python main.py" > ~/$SCRIPT_NAME

chmod +x ~/$SCRIPT_NAME

if ! grep -q "alias $ALIAS_NAME=" "$SHELL_RC"; then
    echo "alias $ALIAS_NAME='~/$SCRIPT_NAME'" >> "$SHELL_RC"
fi

source "$SHELL_RC"

echo "Setup complete. You can now run the script with the command: $ALIAS_NAME"
