#!/usr/bin/env python3
"""
Deployment script for Resume Relevance Check System
"""

import os
import subprocess
import sys
from pathlib import Path

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

def check_git_status():
    """Check if git is initialized and files are committed"""
    if not Path(".git").exists():
        print("📁 Initializing git repository...")
        if not run_command("git init", "Git initialization"):
            return False
    
    # Check if there are uncommitted changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Uncommitted changes detected. Please commit them first.")
        print("Run: git add . && git commit -m 'Your commit message'")
        return False
    
    return True

def deploy_streamlit_cloud():
    """Deploy to Streamlit Cloud"""
    print("🚀 Deploying to Streamlit Cloud...")
    print("\n📋 Steps to deploy:")
    print("1. Go to https://share.streamlit.io")
    print("2. Sign in with your GitHub account")
    print("3. Click 'New app'")
    print("4. Select your repository")
    print("5. Set main file path: streamlit_app.py")
    print("6. Click 'Deploy'")
    print("\n✨ Your app will be available at: https://your-app-name.streamlit.app")

def deploy_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("❌ Heroku CLI not found. Please install it first:")
        print("https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Create Heroku app
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    if app_name:
        if not run_command(f"heroku create {app_name}", f"Creating Heroku app '{app_name}'"):
            return False
    else:
        if not run_command("heroku create", "Creating Heroku app"):
            return False
    
    # Deploy
    if not run_command("git push heroku main", "Deploying to Heroku"):
        return False
    
    print("✅ Deployment successful!")
    print("🌐 Your app is now live on Heroku!")

def deploy_docker():
    """Deploy using Docker"""
    print("🐳 Building Docker image...")
    
    if not run_command("docker build -t resume-checker .", "Building Docker image"):
        return False
    
    print("🚀 Starting Docker container...")
    if not run_command("docker run -d -p 8501:8501 --name resume-checker-app resume-checker", "Starting container"):
        return False
    
    print("✅ Docker deployment successful!")
    print("🌐 Your app is running at: http://localhost:8501")
    print("📋 To stop: docker stop resume-checker-app")
    print("📋 To remove: docker rm resume-checker-app")

def main():
    """Main deployment function"""
    print("🎯 Resume Relevance Check System - Deployment Tool")
    print("=" * 50)
    
    # Check git status
    if not check_git_status():
        return
    
    print("\n🚀 Choose deployment option:")
    print("1. Streamlit Cloud (Recommended - Free)")
    print("2. Heroku")
    print("3. Docker (Local)")
    print("4. Show deployment guide")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        deploy_streamlit_cloud()
    elif choice == "2":
        deploy_heroku()
    elif choice == "3":
        deploy_docker()
    elif choice == "4":
        print("\n📖 Deployment Guide:")
        print("Check README_DEPLOYMENT.md for detailed instructions")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
