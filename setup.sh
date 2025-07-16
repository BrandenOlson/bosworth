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

#!/bin/bash

echo "📦 Pulling models defined in ollama_models.py..."

# Read models from Python output, line by line
MODELS=$(python3 bosworth/ollama_models.py)

# Pull each model
echo "$MODELS" | while IFS= read -r model; do
  echo "  ➤ Pulling $model..."
  ollama pull "$model"
done

# Verify models are registered
echo "🧪 Verifying models are registered..."
OLLAMA_LIST=$(ollama list)
MISSING=false

echo "$MODELS" | while IFS= read -r model; do
  if echo "$OLLAMA_LIST" | grep -q "$model"; then
    echo "  ✅ $model is registered"
  else
    echo "  ❌ $model is NOT registered"
    MISSING=true
  fi
done

if [ "$MISSING" = true ]; then
  echo "⚠️ One or more models are missing."
else
  echo "🎉 Setup complete!"
  echo "➡️ Models are ready to use via http://localhost:11434"
fi

echo "🎉 Setup complete!"
COMMA_SEPARATED_MODELS=$(echo "$MODELS" | paste -sd, - | sed "s/,/, /g")
echo "➡️ All models in {$COMMA_SEPARATED_MODELS} are ready to use via http://localhost:11434"