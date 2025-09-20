#!/usr/bin/env python3
"""
Test to verify text colors are correct
"""

import streamlit as st

st.set_page_config(
    page_title="Color Test",
    page_icon="🎨",
    layout="wide"
)

# Apply the same CSS
st.markdown("""
<style>
/* Main app styling - Clean white background */
.stApp {
    background: #ffffff;
    font-family: Arial, sans-serif;
    color: #000000;
}

/* Ensure all text is black by default */
body, p, div, span, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* Override for header only */
.main-header h1, .main-header p {
    color: white !important;
}

/* Header styling - Simple black header */
.main-header {
    background: #000000;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    border: 2px solid #000000;
}

/* Sidebar styling - Simple white */
.stSidebar {
    background: #ffffff;
    border-right: 2px solid #000000;
    color: #000000;
}

/* Ensure sidebar text is black */
.stSidebar p, .stSidebar div, .stSidebar span, .stSidebar h1, .stSidebar h2, .stSidebar h3 {
    color: #000000 !important;
}

/* Main content area text */
.main .block-container {
    color: #000000;
}

.main .block-container p, .main .block-container div, .main .block-container span {
    color: #000000 !important;
}

/* Streamlit specific text elements */
.stMarkdown, .stText, .stSelectbox label, .stTextInput label, .stTextArea label {
    color: #000000 !important;
}

.stMarkdown p, .stMarkdown div, .stMarkdown span {
    color: #000000 !important;
}

/* Ensure all Streamlit text is black */
.stApp .stMarkdown, .stApp .stText, .stApp .stSelectbox, .stApp .stTextInput, .stApp .stTextArea {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# Test header (should be white text on black background)
st.markdown("""
<div class="main-header">
    <h1>🎯 Header Test</h1>
    <p>This text should be WHITE on black background</p>
</div>
""", unsafe_allow_html=True)

# Test regular text (should be black text on white background)
st.title("📝 Regular Text Test")
st.write("This text should be BLACK on white background")
st.info("This info box text should be BLACK")
st.success("This success message should be BLACK")
st.warning("This warning should be BLACK")
st.error("This error should be BLACK")

# Test sidebar
with st.sidebar:
    st.write("Sidebar text should be BLACK")
    st.selectbox("Select option", ["Option 1", "Option 2"])
    st.text_input("Enter text")

st.write("✅ Color Test Complete!")
st.write("Header text should be WHITE, all other text should be BLACK")
