#!/bin/bash
# debug_app.sh - Script to launch the Flask app in debug mode

# Make sure debugpy is installed
python -m pip install debugpy

# Start the Flask app with debugpy listening on port 5678
# --wait-for-client makes the script pause until VS Code connects
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py

# Note: The app will pause execution until you connect with VS Code debugger
# Use the "Python: Attach" configuration in VS Code to connect
