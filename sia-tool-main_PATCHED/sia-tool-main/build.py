#!/usr/bin/env python3
"""
Build script for Signal Integrity Assessment
Builds the React frontend using npm
"""

import subprocess
import sys
import os
import shutil

def run_command(command, cwd=None):
    """Run a shell command and handle errors"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("=" * 60)
    print("Building Signal Integrity Assessment")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('client'):
        print("ERROR: 'client' directory not found!")
        print("Make sure you're running this from the project root.")
        sys.exit(1)
    
    # Install Python dependencies
    print("\n[1/4] Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install Python dependencies")
        sys.exit(1)
    
    # Install npm dependencies
    print("\n[2/4] Installing npm dependencies...")
    if not run_command("npm install"):
        print("Failed to install npm dependencies")
        sys.exit(1)
    
    # Build React app
    print("\n[3/4] Building React frontend...")
    if not run_command("npm run build:client"):
        print("Failed to build React app")
        sys.exit(1)
    
    # Move build to dist folder
    print("\n[4/4] Organizing build output...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    if os.path.exists('client/dist'):
        shutil.copytree('client/dist', 'dist')
        print("Frontend built successfully to dist/")
    else:
        print("ERROR: client/dist not found after build")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Build completed successfully!")
    print("=" * 60)
    print("\nYou can now run the app with:")
    print("  python app.py")
    print("\nOr for production:")
    print("  gunicorn app:app")

if __name__ == '__main__':
    main()
