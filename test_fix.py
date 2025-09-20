#!/usr/bin/env python3
"""
Test to verify the text visibility fix
"""

import streamlit as st

st.set_page_config(
    page_title="Text Fix Test",
    page_icon="🔧",
    layout="wide"
)

# Apply the same CSS as the main app
st.markdown("""
<style>
/* ===== MAIN APP BACKGROUND ===== */
.stApp {
    background: #ffffff;
    font-family: Arial, sans-serif;
}

/* ===== HEADER SECTION (BLACK BACKGROUND) ===== */
.main-header {
    background: #000000;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    border: 2px solid #000000;
}

.main-header h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0;
    color: white !important;
}

.main-header p {
    font-size: 1.1rem;
    margin: 0.5rem 0 0 0;
    color: white !important;
}

/* ===== SIDEBAR (WHITE BACKGROUND) ===== */
.stSidebar {
    background: #ffffff;
    border-right: 2px solid #000000;
}

/* ===== MAIN CONTENT AREA (WHITE BACKGROUND) ===== */
.main .block-container {
    background: #ffffff;
    color: #000000;
}

/* ===== FORCE ALL TEXT TO BE BLACK ===== */
* {
    color: #000000 !important;
}

/* Override for header only */
.main-header * {
    color: white !important;
}

/* Override for buttons */
.stButton button {
    color: white !important;
}

/* Override for selected tabs */
.stTabs [aria-selected="true"] {
    color: white !important;
}

/* Streamlit specific overrides */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #000000 !important;
}

/* Force all labels to be black */
label, .stSelectbox label, .stTextInput label, .stTextArea label, .stRadio label, .stFileUploader label {
    color: #000000 !important;
}

/* Force all text inputs to have black text */
input, textarea, select {
    color: #000000 !important;
}

/* Target specific Streamlit elements that are showing as light gray */
.stRadio > label, .stRadio > div > label {
    color: #000000 !important;
}

.stSelectbox > label, .stSelectbox > div > label {
    color: #000000 !important;
}

.stTextInput > label, .stTextInput > div > label {
    color: #000000 !important;
}

.stTextArea > label, .stTextArea > div > label {
    color: #000000 !important;
}

.stFileUploader > label, .stFileUploader > div > label {
    color: #000000 !important;
}

/* Force all div and span text to be black */
div, span, p, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* Override Streamlit's default light gray text */
.stApp div, .stApp span, .stApp p {
    color: #000000 !important;
}

/* Target the specific elements causing issues */
.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
}

.stTabs [data-baseweb="tab"] span {
    color: #000000 !important;
}

/* Target Streamlit's specific light gray text classes */
.stApp [data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

.stApp [data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
}

.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3,
.stApp [data-testid="stMarkdownContainer"] h4,
.stApp [data-testid="stMarkdownContainer"] h5,
.stApp [data-testid="stMarkdownContainer"] h6 {
    color: #000000 !important;
}

/* Force all text in the main content area to be black */
.main .block-container * {
    color: #000000 !important;
}

/* Override for header */
.main .block-container .main-header * {
    color: white !important;
}

/* Force sidebar text to be black */
.stSidebar * {
    color: #000000 !important;
}

/* ===== FORM ELEMENTS (BLACK TEXT) ===== */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    color: #000000 !important;
    background: #ffffff !important;
    border: 2px solid #000000 !important;
}

/* ===== BUTTONS (BLACK BACKGROUND, WHITE TEXT) ===== */
.stButton button {
    background: #000000 !important;
    color: white !important;
    border: 2px solid #000000 !important;
    border-radius: 5px !important;
}

.stButton button:hover {
    background: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #000000 !important;
}

/* ===== TABS (WHITE BACKGROUND, BLACK TEXT) ===== */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border: 2px solid #000000 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
    background: #ffffff !important;
}

.stTabs [aria-selected="true"] {
    background: #000000 !important;
    color: white !important;
}

/* ===== CARDS AND CONTAINERS (WHITE BACKGROUND, BLACK TEXT) ===== */
.metric-card, .success-card, .metric-container {
    background: #ffffff !important;
    border: 2px solid #000000 !important;
    color: #000000 !important;
}

.metric-card p, .success-card p, .metric-container p {
    color: #000000 !important;
}

/* ===== ALERT MESSAGES (KEEP STREAMLIT DEFAULTS) ===== */
.stAlert {
    border: 2px solid #000000 !important;
}

/* ===== FILE UPLOADER (WHITE BACKGROUND, BLACK BORDER) ===== */
.stFileUploader > div {
    background: #ffffff !important;
    border: 2px dashed #000000 !important;
}

/* ===== PROGRESS BAR (BLACK PROGRESS) ===== */
.stProgress > div > div > div > div {
    background: #000000 !important;
}

/* ===== EXPANDERS (WHITE BACKGROUND, BLACK TEXT) ===== */
.streamlit-expanderHeader {
    background: #ffffff !important;
    border: 2px solid #000000 !important;
    color: #000000 !important;
}

.streamlit-expanderContent {
    background: #ffffff !important;
    color: #000000 !important;
}

/* ===== SCROLLBAR (BLACK SCROLLBAR) ===== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f0f0f0;
}

::-webkit-scrollbar-thumb {
    background: #000000;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #333333;
}
</style>
""", unsafe_allow_html=True)

# Test header (should be WHITE text on BLACK background)
st.markdown("""
<div class="main-header">
    <h1>🎯 Header Test</h1>
    <p>This should be WHITE text on BLACK background</p>
</div>
""", unsafe_allow_html=True)

# Test sidebar
with st.sidebar:
    st.write("Sidebar text should be BLACK")
    st.selectbox("Select option", ["Option 1", "Option 2"])
    st.radio("Choose", ["A", "B", "C"])

# Test main content (should be BLACK text on WHITE background)
st.title("📝 Main Content Test")
st.write("This text should be BLACK on white background")

# Test form elements
st.subheader("📋 Form Elements Test")
col1, col2 = st.columns(2)

with col1:
    st.text_input("Text input (should be BLACK text)")
    st.text_area("Text area (should be BLACK text)")

with col2:
    st.selectbox("Select box (should be BLACK text)", ["Option 1", "Option 2"])
    st.file_uploader("File uploader (should have BLACK border)")

# Test buttons
st.subheader("🔘 Buttons Test")
st.button("Button (should be WHITE text on BLACK background)")

# Test tabs
st.subheader("📑 Tabs Test")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("Tab 1 content should be BLACK text")
with tab2:
    st.write("Tab 2 content should be BLACK text")
with tab3:
    st.write("Tab 3 content should be BLACK text")

# Test alerts
st.subheader("🚨 Alert Messages Test")
st.info("Info message should be BLACK text")
st.success("Success message should be BLACK text")
st.warning("Warning message should be BLACK text")
st.error("Error message should be BLACK text")

st.write("✅ **FIXED!** All text should now be BLACK and readable!")
