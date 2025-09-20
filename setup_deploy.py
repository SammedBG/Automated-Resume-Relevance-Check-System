#!/usr/bin/env python3
"""
Setup script for deployment
Downloads required models and data
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_models():
    """Download required models and data"""
    print("🚀 Setting up models for deployment...")
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("⚠️ spaCy model download failed, but continuing...")
    
    # Download NLTK data
    if not run_command("python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"", "Downloading NLTK data"):
        print("⚠️ NLTK data download failed, but continuing...")
    
    print("✅ Setup completed!")

if __name__ == "__main__":
    setup_models()
