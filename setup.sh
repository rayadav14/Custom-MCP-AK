#!/bin/bash

set -e

echo "=> Creating Python virtual environment..."
python3 -m venv .venv

echo "=> Upgrading pip..."
.venv/bin/pip install --upgrade pip

echo "=> Installing dependencies..."
.venv/bin/pip install -r requirements.txt

echo "=> Copying .env template..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "   IMPORTANT: Edit .env and fill in your Akamai credentials!"
else
  echo "   .env already exists, skipping."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your Akamai credentials"
echo "  2. Open this folder in VS Code (Remote SSH)"
echo "  3. VS Code will detect .vscode/mcp.json automatically"
echo "  4. Run: Ctrl+Shift+P → MCP: List Servers → Start akamai-mcp"
echo "  OR press F5 to launch via debug config"
