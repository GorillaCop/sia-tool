#!/bin/bash

# Signal Integrity Assessment - Quick Start Script

echo "🎯 Signal Integrity Assessment™"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r streamlit_requirements.txt
    echo ""
fi

echo "✓ Dependencies installed"
echo ""

# Run the application
echo "🚀 Starting Signal Integrity Assessment..."
echo ""
echo "The application will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py
