#!/bin/bash

if ! command -v cargo &> /dev/null; then
    echo "Installing via Rustup..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust is already installed."
fi

if ! command -v kotlinc &> /dev/null; then
    echo "Kotlin not found."
    if command -v brew &> /dev/null; then
        echo "Installing Kotlin via Homebrew..."
        brew install kotlin
    elif command -v sdk &> /dev/null; then
        echo "Installing Kotlin via SDKMAN..."
        sdk install kotlin
    else
        curl -s "https://get.sdkman.io" | bash
        source "$HOME/.sdkman/bin/sdkman-init.sh"
        sdk install kotlin
    fi
else
    echo "Kotlin is already installed."
fi

echo "Complete. Run 'source ~/.zshrc' or restart terminal if commands are not found."
