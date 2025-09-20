#!/usr/bin/env python3
"""
Setup script for Resume Relevance Check System
This script handles the initial setup and dependency installation
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def install_requirements():
    """Install Python requirements with error handling"""
    print("📦 Installing Python requirements...")
    
    # First, upgrade pip
    print("Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install requirements with retries for problematic packages
    try:
        # Install core dependencies first
        core_deps = [
            "streamlit==1.28.1",
            "pandas==2.1.3",
            "numpy==1.24.3",
            "scikit-learn==1.3.2"
        ]
        
        for dep in core_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}"):
                print(f"⚠️ Failed to install {dep}, continuing...")
        
        # Install file processing dependencies
        file_deps = [
            "PyMuPDF==1.23.8",
            "pdfplumber==0.10.3", 
            "python-docx==0.8.11",
            "openpyxl==3.1.2"
        ]
        
        for dep in file_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}"):
                print(f"⚠️ Failed to install {dep}, continuing...")
        
        # Install NLP dependencies
        nlp_deps = [
            "spacy==3.7.2",
            "nltk==3.8.1",
            "fuzzywuzzy==0.18.0",
            "python-Levenshtein==0.21.1"
        ]
        
        for dep in nlp_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}"):
                print(f"⚠️ Failed to install {dep}, continuing...")
        
        # Try to install sentence-transformers (optional)
        print("📦 Installing sentence-transformers (optional for semantic matching)...")
        if not run_command(f"{sys.executable} -m pip install sentence-transformers==2.7.0"):
            print("⚠️ sentence-transformers installation failed. Semantic matching will use TF-IDF fallback.")
        
        # Try to install python-magic-bin (Windows-friendly)
        print("📦 Installing python-magic-bin (optional for file validation)...")
        if not run_command(f"{sys.executable} -m pip install python-magic-bin==0.4.14"):
            print("⚠️ python-magic-bin installation failed. File validation will use basic checks.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def download_spacy_model():
    """Download spaCy English model"""
    print("🔤 Downloading spaCy English model...")
    try:
        result = run_command(f"{sys.executable} -m spacy download en_core_web_sm")
        if not result:
            print("⚠️ spaCy model download failed. NLP features may be limited.")
        return result
    except Exception as e:
        print(f"⚠️ spaCy model download failed: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️ NLTK download failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'exports', 'logs', 'sample_data', 'sample_data/resumes', 'sample_data/job_descriptions']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def test_imports():
    """Test critical imports"""
    print("🧪 Testing critical imports...")
    
    critical_imports = [
        ('streamlit', 'Streamlit web framework'),
        ('pandas', 'Data manipulation'),
        ('numpy', 'Numerical computing'),
        ('sklearn', 'Machine learning'),
    ]
    
    optional_imports = [
        ('sentence_transformers', 'Semantic matching (will use TF-IDF fallback)'),
        ('magic', 'File validation (will use basic checks)'),
        ('spacy', 'Advanced NLP (will use basic patterns)'),
    ]
    
    all_good = True
    
    for module, description in critical_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} - REQUIRED")
            all_good = False
    
    for module, description in optional_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"⚠️ {module} - {description} - OPTIONAL")
    
    return all_good

def main():
    """Main setup function"""
    print("🚀 Setting up Resume Relevance Check System...")
    print("=" * 50)
    
    # Install requirements
    install_success = install_requirements()
    
    # Download models (optional)
    spacy_success = download_spacy_model()
    nltk_success = download_nltk_data()
    
    # Create directories
    create_directories()
    
    # Test imports
    import_success = test_imports()
    
    print("=" * 50)
    if import_success:
        print("✅ Setup completed successfully!")
        print("\nTo run the application:")
        print("streamlit run app.py")
        print("\nTo create sample data:")
        print("python sample_data/create_samples.py")
        print("\nTo run tests:")
        print("python run_tests.py")
    else:
        print("❌ Setup completed with critical errors.")
        print("Please install missing critical dependencies manually.")
        return 1
    
    if not (spacy_success and nltk_success):
        print("\n⚠️ Some optional components failed to install.")
        print("The system will work with reduced functionality.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())