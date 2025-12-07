#!/bin/bash

# Optional: print Python version
echo "Python version: $(python --version)"

# Install requirements
pip install -r requirements.txt

# Launch backend on the port provided by Render
uvicorn backend:app --host 0.0.0.0 --port $PORT
