#!/usr/bin/env python3
"""
SafeWatch AI Setup Script

Automated setup and verification script for the industrial accident detection system.
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n📋 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python version compatible")
        return True
    else:
        print("❌ Python 3.10+ required")
        return False

def main():
    """Main setup process."""
    print("🛡️  SafeWatch AI - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check if config exists
    config_path = Path("config/camera_config.json")
    if config_path.exists():
        print("✅ Configuration file found")
    else:
        print("❌ Configuration file missing")
        sys.exit(1)
    
    # Check if YOLO model exists (will be auto-downloaded)
    model_path = Path("yolov8n.pt")
    if model_path.exists():
        print("✅ YOLO model found")
    else:
        print("ℹ️  YOLO model will be auto-downloaded on first run")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Configure email alerts (optional):")
    print("   cp .env.example .env")
    print("   # Edit .env with your SMTP credentials")
    print("\n2. Run the application:")
    print("   Web Dashboard: streamlit run dashboard/app.py")
    print("   CLI Mode:     python main.py")
    print("\n3. Access dashboard at: http://localhost:8501")

if __name__ == "__main__":
    main()
