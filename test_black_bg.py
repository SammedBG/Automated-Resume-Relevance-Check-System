#!/usr/bin/env python3
"""
Test to verify all black background areas have white text
"""

import streamlit as st

st.set_page_config(
    page_title="Black Background Test",
    page_icon="⚫",
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

/* Override for any element with black background */
[style*="background: #000000"] *,
[style*="background:#000000"] * {
    color: white !important;
}

/* Specific overrides for black background elements */
div[style*="background: #000000"],
div[style*="background:#000000"] {
    color: white !important;
}

div[style*="background: #000000"] *,
div[style*="background:#000000"] * {
    color: white !important;
}

/* Specific classes for black background elements */
.black-bg, .processing-status, .success-message {
    background: #000000 !important;
    color: white !important;
}

.black-bg *, .processing-status *, .success-message * {
    color: white !important;
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
</style>
""", unsafe_allow_html=True)

# Test 1: Header (should be WHITE text on BLACK background)
st.markdown("""
<div class="main-header">
    <h1>🎯 Header Test</h1>
    <p>This should be WHITE text on BLACK background</p>
</div>
""", unsafe_allow_html=True)

# Test 2: Inline black background div (should be WHITE text)
st.markdown("""
<div style="background: #000000; padding: 2rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
    <h2>Processing Status</h2>
    <p>This should be WHITE text on BLACK background</p>
    <div>All text in this black box should be WHITE</div>
</div>
""", unsafe_allow_html=True)

# Test 3: Buttons (should be WHITE text on BLACK background)
st.subheader("🔘 Buttons Test")
st.button("Button 1 (should be WHITE text on BLACK background)")
st.button("Button 2 (should be WHITE text on BLACK background)")

# Test 4: Tabs (selected tab should be WHITE text on BLACK background)
st.subheader("📑 Tabs Test")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("Tab 1 content should be BLACK text")
with tab2:
    st.write("Tab 2 content should be BLACK text")
with tab3:
    st.write("Tab 3 content should be BLACK text")

# Test 5: Another black background div
st.markdown("""
<div style="background: #000000; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
    <h3>Another Black Background</h3>
    <p>This text should be WHITE</p>
    <span>This span should also be WHITE</span>
</div>
""", unsafe_allow_html=True)

# Test 6: Regular content (should be BLACK text on WHITE background)
st.subheader("📝 Regular Content Test")
st.write("This text should be BLACK on white background")
st.info("This info should be BLACK text")
st.success("This success should be BLACK text")

st.write("✅ **BLACK BACKGROUND TEST COMPLETE!**")
st.write("**Expected Results:**")
st.write("- Header: WHITE text on BLACK background")
st.write("- Black background divs: WHITE text")
st.write("- Buttons: WHITE text on BLACK background")
st.write("- Selected tabs: WHITE text on BLACK background")
st.write("- Everything else: BLACK text on WHITE background")
