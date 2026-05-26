#!/bin/bash
# ============================================
# SQL Injection Demo App — One-Click Launcher
# IIT Jodhpur | Cyber Security Assignment
# ============================================

echo "======================================"
echo "  SQL Injection Demo App - IIT Jodhpur"
echo "======================================"
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
    echo "      ✅ Virtual environment created"
else
    echo "[1/3] Virtual environment already exists ✅"
fi

# Activate and install Flask
echo "[2/3] Installing Flask..."
source venv/bin/activate
pip install flask --quiet
echo "      ✅ Flask installed"

# Initialize DB and run
echo "[3/3] Starting the web app..."
echo ""
echo "======================================"
echo "  🌐 Open in your browser:"
echo "  http://localhost:5000"
echo "======================================"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""

python app.py
