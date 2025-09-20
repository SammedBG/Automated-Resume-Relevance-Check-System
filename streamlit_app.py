"""
Streamlit app entry point for deployment
This file is used by Streamlit Cloud for deployment
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import the main app
    from app_clean import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    # Handle missing dependencies gracefully
    st.error(f"❌ Import error: {e}")
    st.info("Some dependencies might be missing. The app will run with limited functionality.")
    
    # Show a basic interface
    st.title("🎯 Resume Relevance Check System")
    st.info("⚠️ Some features may not be available due to missing dependencies.")
    st.write("Please check the deployment logs for more information.")
    
    # Try to run setup
    if st.button("🔄 Try to install missing dependencies"):
        with st.spinner("Installing dependencies..."):
            import subprocess
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Dependencies installed successfully! Please refresh the page.")
                else:
                    st.error(f"❌ Installation failed: {result.stderr}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
