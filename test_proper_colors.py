#!/usr/bin/env python3
"""
Comprehensive test to verify proper color scheme
"""

import streamlit as st

st.set_page_config(
    page_title="Proper Color Test",
    page_icon="🎨",
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

.stSidebar .stMarkdown {
    color: #000000 !important;
}

.stSidebar .stSelectbox label {
    color: #000000 !important;
}

.stSidebar .stRadio label {
    color: #000000 !important;
}

/* ===== MAIN CONTENT AREA (WHITE BACKGROUND) ===== */
.main .block-container {
    background: #ffffff;
    color: #000000;
}

/* ===== STREAMLIT TEXT ELEMENTS (BLACK TEXT) ===== */
.stMarkdown {
    color: #000000 !important;
}

.stMarkdown p {
    color: #000000 !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #000000 !important;
}

/* ===== FORM ELEMENTS (BLACK TEXT) ===== */
.stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {
    color: #000000 !important;
}

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
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Button 1 (should be WHITE text on BLACK background)")
with col2:
    st.button("Button 2 (should be WHITE text on BLACK background)")
with col3:
    st.button("Button 3 (should be WHITE text on BLACK background)")

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

# Test expanders
st.subheader("📂 Expanders Test")
with st.expander("Expand me"):
    st.write("Expanded content should be BLACK text")

# Test progress bar
st.subheader("📊 Progress Bar Test")
st.progress(0.7)

# Test cards
st.subheader("🃏 Cards Test")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="metric-card">
        <p>Card content should be BLACK text</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="success-card">
        <p>Success card should be BLACK text</p>
    </div>
    """, unsafe_allow_html=True)

st.write("✅ Color Test Complete!")
st.write("**Expected Results:**")
st.write("- Header: WHITE text on BLACK background")
st.write("- Everything else: BLACK text on WHITE background")
st.write("- Buttons: WHITE text on BLACK background")
st.write("- Selected tabs: WHITE text on BLACK background")
