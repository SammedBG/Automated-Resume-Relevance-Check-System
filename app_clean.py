"""
Enhanced Resume Relevance Check System
Professional Streamlit-only application
"""

import streamlit as st

# Configure page settings - MUST be first Streamlit command
st.set_page_config(
    page_title="Resume Relevance Check System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import json
from datetime import datetime
import os
import re
from pathlib import Path
import time

# Import with error handling
try:
    from resume_processor import ResumeProcessor
    from database import DatabaseManager
    from utils import export_results
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.info("Please run: python setup.py")
    COMPONENTS_AVAILABLE = False

def apply_custom_css():
    """Apply clean white and black styling with proper icon styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling - Clean white background */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling - Clean black header */
    .main-header {
        background: #000000;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        border: 2px solid #e0e0e0;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
     .main-header h1 {
         font-size: 3rem;
         font-weight: 700;
         margin: 0;
         color: white !important;
         text-shadow: 0 2px 4px rgba(0,0,0,0.3);
         position: relative;
         z-index: 1;
     }
     
     .main-header p {
         font-size: 1.2rem;
         font-weight: 300;
         margin: 0.5rem 0 0 0;
         color: white !important;
         opacity: 0.9;
         position: relative;
         z-index: 1;
     }
     
     .main-header * {
         color: white !important;
     }
    
    /* Sidebar styling - Clean white */
    .stSidebar {
        background: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
    
    /* Card styling - Clean white cards with black borders */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-color: #000000;
    }
    
    .success-card {
        background: #ffffff;
        border: 2px solid #000000;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Progress bar styling - Black progress bar */
    .stProgress > div > div > div > div {
        background: #000000;
        border-radius: 10px;
    }
    
    /* Button styling - Black buttons with white text */
    .stButton > button {
        background: #000000;
        color: white;
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background: #ffffff;
        color: #000000;
        border-color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* File uploader styling - Clean white with black border */
    .stFileUploader > div {
        background: #ffffff;
        border: 2px dashed #000000;
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #333333;
        background: #f8f8f8;
        border-style: solid;
    }
    
    /* Input styling - Clean white inputs with black borders */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within {
        border-color: #000000;
        box-shadow: 0 0 0 3px rgba(0,0,0,0.1);
    }
    
    /* Tab styling - Clean white tabs with black selection */
    .stTabs [data-baseweb="tab-list"] {
        background: #ffffff;
        border-radius: 15px;
        padding: 0.5rem;
        border: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #000000;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #000000;
        color: white;
    }
    
    /* Expander styling - Clean white expanders */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
    }
    
    /* Metric styling - Clean white metric containers */
    .metric-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
        border-color: #000000;
    }
    
    /* Loading animation - Black spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #e0e0e0;
        border-radius: 50%;
        border-top-color: #000000;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Success animation - Black checkmark */
    .success-checkmark {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #000000;
        position: relative;
        animation: checkmark 0.6s ease-in-out;
    }
    
    .success-checkmark::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
    }
    
    @keyframes checkmark {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    /* Floating elements */
    .floating-element {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Custom scrollbar - Black scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f0f0f0;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #000000;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #333333;
    }
    </style>
    
    <script>
    // Add interactive features
    document.addEventListener('DOMContentLoaded', function() {
        // Add click animations to buttons
        const buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            });
        });
        
        // Add hover effects to cards
        const cards = document.querySelectorAll('.metric-card, .success-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
        
        // Add typing animation to status text
        function typeWriter(element, text, speed = 50) {
            let i = 0;
            element.innerHTML = '';
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def main():
    """Enhanced main application"""
    apply_custom_css()
    
    # Modern attractive header
    st.markdown("""
    <div class="main-header floating-element">
        <h1 style="color: white !important;">🎯 Resume Relevance Check System</h1>
        <p style="color: white !important;">AI-powered resume evaluation and gap analysis</p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: white !important;">✨ Smart Analysis</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: white !important;">🚀 Fast Processing</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: white !important;">📊 Detailed Reports</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not COMPONENTS_AVAILABLE:
        st.error("❌ System components not available. Please run setup first.")
        st.code("python setup.py", language="bash")
        return
    
    # Initialize components
    if 'processor' not in st.session_state:
        try:
            st.session_state.processor = ResumeProcessor()
            st.session_state.db = DatabaseManager()
        except Exception as e:
            st.error(f"❌ Failed to initialize components: {e}")
            return
    
    # Enhanced sidebar with modern styling
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #000000; margin: 0; font-weight: 700;">🧭 Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox("Choose a page", 
                           ["🚀 Upload & Process", "📊 Results Dashboard", "📈 Analytics"],
                           format_func=lambda x: x)
        
        st.markdown("---")
        
        # Processing configuration with enhanced styling
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h4 style="color: #000000; margin: 0; font-weight: 600;">⚙️ Processing Configuration</h4>
        </div>
        """, unsafe_allow_html=True)
        
        processing_mode = st.radio(
            "Processing Mode:",
            ["Standard (Fast)", "Advanced (LLM)", "Hybrid"],
            index=0,
            help="Standard: Fast keyword matching | Advanced: AI analysis | Hybrid: Best of both"
        )
        
        # Enhanced scoring weights section
        with st.expander("🎯 Scoring Weights", expanded=False):
            st.markdown("""
            <div style="background: #f8f8f8; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #e0e0e0;">
                <p style="margin: 0; font-size: 0.9rem; color: #000000;">
                    Adjust the balance between exact keyword matching and semantic similarity analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            hard_weight = st.slider("Hard Match Weight", 0.0, 1.0, 0.6, 0.1,
                                   help="Weight for exact keyword matches")
            semantic_weight = st.slider("Semantic Match Weight", 0.0, 1.0, 0.4, 0.1,
                                      help="Weight for semantic similarity")
            
            # Normalize weights
            total_weight = hard_weight + semantic_weight
            if total_weight > 0:
                hard_weight = hard_weight / total_weight
                semantic_weight = semantic_weight / total_weight
            
            # Visual weight representation
            st.markdown(f"""
            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                <div style="flex: {hard_weight}; background: #000000; height: 8px; border-radius: 4px;"></div>
                <div style="flex: {semantic_weight}; background: #666666; height: 8px; border-radius: 4px;"></div>
            </div>
            <p style="text-align: center; margin: 0.5rem 0; font-size: 0.8rem; color: #000000;">
                Hard: {hard_weight:.1%} | Semantic: {semantic_weight:.1%}
            </p>
            """, unsafe_allow_html=True)
        
        # Quick stats with enhanced styling
        if 'db' in st.session_state:
            try:
                all_results = st.session_state.db.get_all_results()
                if all_results:
                    st.markdown("---")
                    st.markdown("""
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <h4 style="color: #000000; margin: 0; font-weight: 600;">📊 Quick Stats</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Processed", len(all_results), delta=None)
                    with col2:
                        high_count = len([r for r in all_results if r.get('verdict') == 'High'])
                        st.metric("High Suitability", high_count, delta=None)
                    
                    # Progress bar for success rate
                    success_rate = (high_count / len(all_results)) * 100 if all_results else 0
                    st.markdown(f"""
                    <div style="margin-top: 1rem;">
                        <p style="margin: 0; font-size: 0.8rem; color: #000000;">Success Rate</p>
                        <div style="background: #e0e0e0; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: #000000; height: 100%; width: {success_rate}%; transition: width 0.3s ease;"></div>
                        </div>
                        <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #000000; text-align: center;">{success_rate:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
    
    st.session_state.hard_weight = hard_weight
    st.session_state.semantic_weight = semantic_weight
    st.session_state.processing_mode = processing_mode
    
    # Display current page
    if page == "🚀 Upload & Process":
        upload_page()
    elif page == "📊 Results Dashboard":
        results_page()
    else:
        analytics_page()

def upload_page():
    """Enhanced upload and processing page"""
    st.header("📤 Upload & Process Resumes")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📋 Job Description", "📄 Resume Upload", "🚀 Process & Results"])
    
    with tab1:
        st.subheader("Job Description")
        
        # Multiple input methods
        input_method = st.radio("Input Method:", ["📁 File Upload", "✏️ Text Input"], horizontal=True)
        
        if input_method == "📁 File Upload":
            uploaded_jd = st.file_uploader(
                "Upload Job Description",
                type=['pdf', 'docx', 'txt'],
                key="job_description",
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if uploaded_jd:
                st.markdown(f"""
                <div class="success-card">
                    ✅ <strong>Job description uploaded:</strong> {uploaded_jd.name}<br>
                    📊 <strong>Size:</strong> {uploaded_jd.size / 1024:.1f} KB
                </div>
                """, unsafe_allow_html=True)
                st.session_state.jd_file = uploaded_jd
                st.session_state.jd_text = None
        else:
            jd_text = st.text_area(
                "Paste Job Description",
                height=200,
                placeholder="Paste the job description here...",
                key="jd_text_input"
            )
            
            if jd_text:
                st.markdown(f"""
                <div class="success-card">
                    ✅ <strong>Job description entered:</strong> {len(jd_text)} characters
                </div>
                """, unsafe_allow_html=True)
                st.session_state.jd_text = jd_text
                st.session_state.jd_file = None
        
        # Job details
        col1, col2 = st.columns(2)
        with col1:
            job_role = st.text_input(
                "Job Role",
                placeholder="e.g., Software Engineer, Data Scientist",
                help="This helps with better analysis"
            )
        with col2:
            company_name = st.text_input(
                "Company Name (Optional)",
                placeholder="e.g., Tech Corp Inc."
            )
        
        st.session_state.job_role = job_role
        st.session_state.company_name = company_name
    
    with tab2:
        st.subheader("Resume Files")
        
        uploaded_resumes = st.file_uploader(
            "Upload Resume Files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            key="resumes",
            help="You can upload multiple resumes at once. Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_resumes:
            st.markdown(f"""
            <div class="success-card">
                ✅ <strong>{len(uploaded_resumes)} resume(s) uploaded</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced file details
            with st.expander("📁 File Details & Preview", expanded=True):
                total_size = sum(resume.size for resume in uploaded_resumes)
                st.info(f"📊 Total size: {total_size / 1024:.1f} KB")
                
                for i, resume in enumerate(uploaded_resumes, 1):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{i}. {resume.name}**")
                    with col2:
                        st.write(f"{resume.size / 1024:.1f} KB")
                    with col3:
                        file_type = resume.name.split('.')[-1].upper()
                        st.write(f"📄 {file_type}")
                
                # Batch naming
                batch_name = st.text_input(
                    "Batch Name (Optional)",
                    placeholder="e.g., Q4 2024 Applications",
                    help="Give this batch a name for easier tracking"
                )
                st.session_state.batch_name = batch_name
    
    with tab3:
        st.subheader("Processing & Results")
        
        # Check if we have both JD and resumes
        has_jd = (hasattr(st.session_state, 'jd_file') and st.session_state.jd_file) or \
                 (hasattr(st.session_state, 'jd_text') and st.session_state.jd_text)
        has_resumes = uploaded_resumes is not None and len(uploaded_resumes) > 0
        
        if has_jd and has_resumes:
            # Enhanced processing configuration summary
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: #000000; margin: 0; font-weight: 700;">🔧 Processing Configuration</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card floating-element">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
                        <strong style="color: #000000;">Mode</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{st.session_state.processing_mode.split()[0]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card floating-element">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚖️</div>
                        <strong style="color: #000000;">Weights</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{st.session_state.hard_weight:.1%} / {st.session_state.semantic_weight:.1%}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                estimated_time = len(uploaded_resumes) * 3
                st.markdown(f"""
                <div class="metric-card floating-element">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏱️</div>
                        <strong style="color: #000000;">Est. Time</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">~{estimated_time}s</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card floating-element">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
                        <strong style="color: #000000;">Resumes</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{len(uploaded_resumes)} files</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Enhanced processing button with animation
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <button onclick="this.style.transform='scale(0.95)'; setTimeout(() => this.style.transform='scale(1)', 150);" 
                            style="background: #000000; 
                                   color: white; border: 2px solid #000000; border-radius: 15px; 
                                   padding: 1rem 3rem; font-size: 1.2rem; font-weight: 600; 
                                   cursor: pointer; transition: all 0.3s ease; 
                                   box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
                        🚀 Start Processing
                    </button>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 Start Processing", type="primary", use_container_width=True):
                    jd_source = st.session_state.get('jd_file') or st.session_state.get('jd_text')
                    process_resumes(uploaded_resumes, jd_source)
        
        else:
            # Show what's missing
            missing_items = []
            if not has_jd:
                missing_items.append("📋 Job Description")
            if not has_resumes:
                missing_items.append("📄 Resume Files")
            
            st.warning(f"⚠️ Missing: {' and '.join(missing_items)}")
        
        # Show current results if available
        if 'current_results' in st.session_state and st.session_state.current_results:
            st.markdown("---")
            st.markdown("### 📊 Latest Results")
            display_results_summary(st.session_state.current_results)

def display_results_summary(results):
    """Display a quick summary of results"""
    if not results:
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", len(results))
    with col2:
        high_count = len([r for r in results if r.get('verdict') == 'High'])
        st.metric("High Suitability", high_count)
    with col3:
        avg_score = sum(r.get('final_score', 0) for r in results) / len(results)
        st.metric("Avg Score", f"{avg_score:.3f}")

def process_resumes(resumes, job_description):
    """Enhanced resume processing with better feedback and animations"""
    # Create processing container with enhanced styling
    processing_container = st.container()
    
    with processing_container:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #000000; margin: 0; font-weight: 700;">🔄 Processing in Progress...</h3>
            <div class="loading-spinner" style="margin: 1rem auto; width: 40px; height: 40px; border-width: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_container = st.empty()
        
        # Processing metrics with enhanced styling
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-container">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <strong style="color: #000000;">Processed</strong>
            </div>
            """, unsafe_allow_html=True)
            processed_metric = st.empty()
        with col2:
            st.markdown("""
            <div class="metric-container">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
                <strong style="color: #000000;">Success</strong>
            </div>
            """, unsafe_allow_html=True)
            success_metric = st.empty()
        with col3:
            st.markdown("""
            <div class="metric-container">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">❌</div>
                <strong style="color: #000000;">Errors</strong>
            </div>
            """, unsafe_allow_html=True)
            error_metric = st.empty()
    
    start_time = time.time()
    
    try:
        # Extract job description
        status_text.markdown("📋 **Extracting job description...**")
        
        if isinstance(job_description, str):
            # Text input
            jd_text = job_description
        else:
            # File input
            jd_text = st.session_state.processor.extract_text_from_file(job_description)
        
        if not jd_text:
            st.error("❌ Failed to extract job description text")
            return
        
        progress_bar.progress(10)
        
        # Initialize counters
        processed_count = 0
        success_count = 0
        error_count = 0
        
        results = []
        total_resumes = len(resumes)
        
        for i, resume_file in enumerate(resumes):
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Enhanced status display with animations
            status_text.markdown(f"""
            <div style="background: #ffffff; padding: 1rem; border-radius: 10px; 
                        border-left: 4px solid #000000; margin: 1rem 0; border: 2px solid #e0e0e0;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div class="loading-spinner" style="width: 20px; height: 20px;"></div>
                    <div>
                        <strong style="color: #000000;">Processing {i+1}/{total_resumes}</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{resume_file.name}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced time display
            eta = (elapsed_time / max(i, 1)) * (total_resumes - i) if i > 0 else 0
            time_container.markdown(f"""
            <div style="background: #f8f8f8; padding: 0.75rem; border-radius: 8px; 
                        text-align: center; margin: 0.5rem 0; border: 1px solid #e0e0e0;">
                <span style="color: #000000; font-weight: 600;">⏱️ Elapsed: {elapsed_time:.1f}s</span> | 
                <span style="color: #666; font-weight: 600;">ETA: {eta:.1f}s</span>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Extract resume text
                resume_text = st.session_state.processor.extract_text_from_file(resume_file)
                
                if resume_text:
                    # Analyze resume
                    analysis = st.session_state.processor.analyze_relevance(
                        resume_text, jd_text,
                        st.session_state.hard_weight,
                        st.session_state.semantic_weight
                    )
                    
                    # Prepare result with enhanced metadata
                    result = {
                        'filename': resume_file.name,
                        'job_role': st.session_state.get('job_role', ''),
                        'company_name': st.session_state.get('company_name', ''),
                        'batch_name': st.session_state.get('batch_name', ''),
                        'processing_mode': st.session_state.processing_mode,
                        'processed_at': datetime.now().isoformat(),
                        'file_size': resume_file.size,
                        **analysis
                    }
                    
                    results.append(result)
                    success_count += 1
                    
                    # Save to database
                    st.session_state.db.save_result(result)
                else:
                    error_count += 1
                    st.warning(f"⚠️ Failed to extract text from {resume_file.name}")
                
            except Exception as e:
                error_count += 1
                st.error(f"❌ Error processing {resume_file.name}: {str(e)}")
            
            processed_count += 1
            
            # Update metrics
            processed_metric.metric("Processed", f"{processed_count}/{total_resumes}")
            success_metric.metric("Success", success_count)
            error_metric.metric("Errors", error_count)
            
            progress_bar.progress(10 + (i + 1) * 80 // total_resumes)
        
        progress_bar.progress(100)
        total_time = time.time() - start_time
        
        # Enhanced completion message with animations
        status_text.markdown("""
        <div style="background: #000000; padding: 2rem; border-radius: 15px; 
                    text-align: center; color: white; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
            <h3 style="margin: 0; font-size: 1.5rem;">Processing Completed Successfully!</h3>
            <div class="success-checkmark" style="margin: 1rem auto; width: 30px; height: 30px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        time_container.markdown(f"""
        <div style="background: #f8f8f8; padding: 1rem; border-radius: 10px; 
                    text-align: center; border: 2px solid #000000;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <strong style="color: #000000;">⏱️ Total Time</strong><br>
                    <span style="color: #666;">{total_time:.1f}s</span>
                </div>
                <div>
                    <strong style="color: #000000;">📊 Avg per Resume</strong><br>
                    <span style="color: #666;">{total_time/total_resumes:.1f}s</span>
                </div>
                <div>
                    <strong style="color: #000000;">🚀 Speed</strong><br>
                    <span style="color: #666;">{total_resumes/total_time:.1f} resumes/s</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Store results
        st.session_state.current_results = results
        
        # Enhanced success summary with animations
        if results:
            st.balloons()  # Celebration animation
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #000000; margin: 0; font-weight: 700;">🎉 Processing Complete!</h2>
                <p style="color: #666; margin: 0.5rem 0;">Your resume analysis is ready for review</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced metrics with better styling
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-container floating-element">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                    <strong style="color: #000000; font-size: 1.1rem;">Total Processed</strong><br>
                    <span style="font-size: 2rem; font-weight: 700; color: #000000;">{len(results)}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                high_count = len([r for r in results if r.get('verdict') == 'High'])
                st.markdown(f"""
                <div class="metric-container floating-element">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
                    <strong style="color: #000000; font-size: 1.1rem;">High Suitability</strong><br>
                    <span style="font-size: 2rem; font-weight: 700; color: #000000;">{high_count}</span>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                avg_score = sum(r.get('final_score', 0) for r in results) / len(results)
                st.markdown(f"""
                <div class="metric-container floating-element">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⭐</div>
                    <strong style="color: #000000; font-size: 1.1rem;">Average Score</strong><br>
                    <span style="font-size: 2rem; font-weight: 700; color: #000000;">{avg_score:.3f}</span>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-container floating-element">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡</div>
                    <strong style="color: #000000; font-size: 1.1rem;">Processing Time</strong><br>
                    <span style="font-size: 2rem; font-weight: 700; color: #000000;">{total_time:.1f}s</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Display results
            display_results(results)
        else:
            st.warning("⚠️ No results generated. Please check your files and try again.")
        
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        st.exception(e)  # Show full traceback in debug mode

def display_results(results):
    """Enhanced display of processing results"""
    st.markdown("---")
    st.header("📊 Detailed Results")
    
    # Enhanced visualizations with tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Detailed List", "📈 Insights"])
    
    with tab1:
        # Score distribution using native Streamlit charts
        scores = [r.get('final_score', 0) for r in results]
        verdicts = [r.get('verdict', 'Unknown') for r in results]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Score Distribution")
            # Create histogram data
            score_df = pd.DataFrame({'Scores': scores})
            st.bar_chart(score_df)
        
        with col2:
            st.subheader("Suitability Distribution")
            # Verdict counts
            verdict_counts = pd.Series(verdicts).value_counts()
            st.bar_chart(verdict_counts)
    
    with tab2:
        # Enhanced filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            verdict_filter = st.selectbox("Filter by Verdict", ["All", "High", "Medium", "Low"])
        
        with col2:
            min_score = st.slider("Minimum Score", 0.0, 1.0, 0.0, 0.05)
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Score (High to Low)", "Score (Low to High)", "Filename", "File Size"])
        
        with col4:
            # Search functionality
            search_term = st.text_input("🔍 Search", placeholder="Search filenames...")
    
        # Apply filters
        filtered_results = results.copy()
        
        # Verdict filter
        if verdict_filter != "All":
            filtered_results = [r for r in filtered_results if r.get('verdict') == verdict_filter]
        
        # Score filter
        filtered_results = [r for r in filtered_results if r.get('final_score', 0) >= min_score]
        
        # Search filter
        if search_term:
            filtered_results = [r for r in filtered_results 
                              if search_term.lower() in r.get('filename', '').lower()]
        
        # Sort results
        if sort_by == "Score (High to Low)":
            filtered_results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        elif sort_by == "Score (Low to High)":
            filtered_results.sort(key=lambda x: x.get('final_score', 0))
        elif sort_by == "File Size":
            filtered_results.sort(key=lambda x: x.get('file_size', 0), reverse=True)
        else:
            filtered_results.sort(key=lambda x: x.get('filename', ''))
        
        st.info(f"Showing {len(filtered_results)} of {len(results)} results")
    
        # Display results with enhanced cards
        if filtered_results:
            for result in filtered_results:
                score = result.get('final_score', 0)
                verdict = result.get('verdict', 'Unknown')
                
                # Color coding
                verdict_colors = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
                verdict_icon = verdict_colors.get(verdict, "⚪")
                
                # Enhanced title with more info
                file_size = result.get('file_size', 0)
                size_kb = file_size / 1024 if file_size else 0
                title = f"{verdict_icon} {result.get('filename', 'Unknown')} - Score: {score:.3f} ({verdict}) | {size_kb:.1f} KB"
                
                with st.expander(title, expanded=(verdict == "High")):
                    # Three column layout
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📊 Scores**")
                        st.write(f"• Final Score: **{score:.3f}**")
                        st.write(f"• Hard Match: {result.get('hard_match_score', 0):.3f}")
                        st.write(f"• Semantic Match: {result.get('semantic_score', 0):.3f}")
                        st.write(f"• Verdict: **{verdict}**")
                    
                    with col2:
                        st.markdown("**🎯 Skills Analysis**")
                        matched_skills = result.get('matched_skills', [])
                        missing_skills = result.get('missing_skills', [])
                        
                        if matched_skills:
                            st.success(f"✅ Matched ({len(matched_skills)}): {', '.join(matched_skills[:3])}")
                            if len(matched_skills) > 3:
                                st.caption(f"... and {len(matched_skills) - 3} more")
                        
                        if missing_skills:
                            st.warning(f"❌ Missing ({len(missing_skills)}): {', '.join(missing_skills[:3])}")
                            if len(missing_skills) > 3:
                                st.caption(f"... and {len(missing_skills) - 3} more")
                    
                    with col3:
                        st.markdown("**📋 Metadata**")
                        st.write(f"• Processed: {result.get('processed_at', 'Unknown')[:16]}")
                        st.write(f"• Mode: {result.get('processing_mode', 'Unknown')}")
                        if result.get('job_role'):
                            st.write(f"• Role: {result.get('job_role')}")
                        if result.get('batch_name'):
                            st.write(f"• Batch: {result.get('batch_name')}")
                    
                    # Suggestions section
                    suggestions = result.get('suggestions', '')
                    if suggestions:
                        st.markdown("**💡 Improvement Suggestions**")
                        st.info(suggestions)
        
        else:
            st.info("No results match the current filters.")
    
    with tab3:
        # Advanced insights using native Streamlit
        if len(results) > 1:
            st.markdown("### 🔍 Advanced Insights")
            
            # Skills analysis
            all_matched_skills = []
            all_missing_skills = []
            
            for result in results:
                all_matched_skills.extend(result.get('matched_skills', []))
                all_missing_skills.extend(result.get('missing_skills', []))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if all_matched_skills:
                    matched_counts = pd.Series(all_matched_skills).value_counts().head(10)
                    st.markdown("**🎯 Most Common Matched Skills**")
                    st.bar_chart(matched_counts)
            
            with col2:
                if all_missing_skills:
                    missing_counts = pd.Series(all_missing_skills).value_counts().head(10)
                    st.markdown("**❌ Most Common Missing Skills**")
                    st.bar_chart(missing_counts)
            
            # Score analysis
            if len(results) > 5:
                st.markdown("**📈 Score Analysis**")
                df_analysis = pd.DataFrame(results)
                
                if 'hard_match_score' in df_analysis.columns and 'semantic_score' in df_analysis.columns:
                    # Create scatter plot data
                    scatter_data = pd.DataFrame({
                        'Hard Match Score': df_analysis['hard_match_score'],
                        'Semantic Score': df_analysis['semantic_score']
                    })
                    st.scatter_chart(scatter_data)
        else:
            st.info("Process more resumes to see advanced insights.")
    
    # Enhanced export options
    st.markdown("---")
    st.markdown("### 📥 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 CSV Export", use_container_width=True):
            df = pd.DataFrame(filtered_results)
            csv = df.to_csv(index=False)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                "📥 Download CSV",
                csv,
                f"resume_analysis_{timestamp}.csv",
                "text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("📋 JSON Export", use_container_width=True):
            json_data = json.dumps(filtered_results, indent=2, default=str)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                "📥 Download JSON",
                json_data,
                f"resume_analysis_{timestamp}.json",
                "application/json",
                use_container_width=True
            )
    
    with col3:
        if st.button("📊 Summary Report", use_container_width=True):
            # Generate summary report
            report_lines = [
                "# Resume Analysis Summary Report",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "## Overview",
                f"- Total Resumes: {len(filtered_results)}",
                f"- High Suitability: {len([r for r in filtered_results if r.get('verdict') == 'High'])}",
                f"- Average Score: {sum(r.get('final_score', 0) for r in filtered_results) / len(filtered_results):.3f}",
                "",
                "## Top Candidates",
            ]
            
            # Add top candidates
            sorted_results = sorted(filtered_results, key=lambda x: x.get('final_score', 0), reverse=True)
            for i, result in enumerate(sorted_results[:5], 1):
                report_lines.append(f"{i}. {result.get('filename', 'Unknown')} - {result.get('final_score', 0):.3f}")
            
            report_content = "\n".join(report_lines)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                "📥 Download Report",
                report_content,
                f"summary_report_{timestamp}.md",
                "text/markdown",
                use_container_width=True
            )

def results_page():
    """Results dashboard page"""
    st.header("📈 Results Dashboard")
    
    try:
        all_results = st.session_state.db.get_all_results()
        
        if not all_results:
            st.info("📭 No results found. Please process some resumes first.")
            return
        
        # Dashboard metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Processed", len(all_results))
        
        with col2:
            high_count = len([r for r in all_results if r.get('verdict') == 'High'])
            st.metric("High Suitability", high_count)
        
        with col3:
            avg_score = sum(r.get('final_score', r.get('score', 0)) for r in all_results) / len(all_results)
            st.metric("Average Score", f"{avg_score:.3f}")
        
        with col4:
            recent_count = len([r for r in all_results if 'created_at' in r])
            st.metric("Recent Batches", recent_count)
        
        # Charts
        st.subheader("📊 Score Distribution")
        scores = [r.get('final_score', r.get('score', 0)) for r in all_results]
        st.bar_chart(pd.DataFrame({'Scores': scores}))
        
        st.subheader("🎯 Verdict Distribution")
        verdict_counts = {}
        for result in all_results:
            verdict = result.get('verdict', 'Unknown')
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        
        st.bar_chart(pd.DataFrame.from_dict(verdict_counts, orient='index', columns=['Count']))
        
        # Recent results
        st.subheader("📋 Recent Results")
        recent_results = all_results[-10:] if len(all_results) > 10 else all_results
        
        df = pd.DataFrame(recent_results)
        if not df.empty:
            # Check which score column exists
            score_col = 'final_score' if 'final_score' in df.columns else 'score'
            display_columns = ['filename', score_col, 'verdict', 'created_at']
            available_columns = [col for col in display_columns if col in df.columns]
            st.dataframe(df[available_columns], use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Failed to load dashboard data: {e}")

def analytics_page():
    """Analytics page"""
    st.header("📊 Advanced Analytics")
    
    try:
        all_results = st.session_state.db.get_all_results()
        
        if not all_results:
            st.info("📭 No data available for analytics.")
            return
        
        # Performance analytics
        st.subheader("🎯 Performance Analytics")
        
        # Score distribution
        scores = [r.get('final_score', r.get('score', 0)) for r in all_results]
        st.bar_chart(pd.DataFrame({'Scores': scores}))
        
        # Processing mode analysis
        st.subheader("⚙️ Processing Mode Analysis")
        mode_counts = {}
        for result in all_results:
            mode = result.get('processing_mode', 'Standard')
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        if mode_counts:
            st.bar_chart(pd.DataFrame.from_dict(mode_counts, orient='index', columns=['Count']))
        
        # Statistics
        st.subheader("📈 Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Processed", len(all_results))
        
        with col2:
            avg_score = sum(r.get('final_score', r.get('score', 0)) for r in all_results) / len(all_results)
            st.metric("Average Score", f"{avg_score:.3f}")
        
        with col3:
            high_percentage = len([r for r in all_results if r.get('verdict') == 'High']) / len(all_results) * 100
            st.metric("High Suitability %", f"{high_percentage:.1f}%")
        
    except Exception as e:
        st.error(f"❌ Analytics failed: {e}")

if __name__ == "__main__":
    main()