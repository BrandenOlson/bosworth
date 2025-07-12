#!/bin/bash

set -e

echo "🔍 Checking for Ollama..."

if ! command -v ollama &> /dev/null; then
  echo "⬇️ Ollama not found, installing via Homebrew..."
  if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is required but not installed. Please install it first: https://brew.sh"
    exit 1
  fi
  brew install ollama
else
  echo "✅ Ollama already installed."
fi

echo "🚦 Checking if Ollama server is running..."
if ! lsof -i :11434 | grep LISTEN &> /dev/null; then
  echo "🚀 Starting Ollama server in background..."
  nohup ollama serve > ollama.log 2>&1 &
  sleep 2  # Give it time to bind
else
  echo "✅ Ollama server already running."
fi

echo "🌐 Verifying API is reachable..."
if curl -s http://localhost:11434 | grep -q "Ollama is running"; then
  echo "✅ Ollama API is up!"
else
  echo "❌ Ollama API failed to respond. Something's wrong."
  exit 1
fi

echo "📦 Pulling supported Ollama models from Python Enum..."
MODELS=$(python3 bosworth/ollama_models.py)

for model in $MODELS; do
  echo "  ➤ Pulling $model..."
  ollama pull "$model"
done

echo "🧪 Verifying models are registered..."
ollama list | grep -E "llama3.2|mistral"

echo "🎉 Setup complete!"
echo "➡️ Models 'llama3.2' and 'mistral' are ready to use via http://localhost:11434"