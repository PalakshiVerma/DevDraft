import os
import streamlit as st
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from api_client import call_polish_api
from styles import CUSTOM_CSS

# Streamlit Page Configuration
st.set_page_config(
    page_title="The Standup & PR Polish Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply sleek styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Backend URL configuration
backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# ----------------- MAIN HEADER -----------------
st.markdown(
    """
    <div style="font-size: 2.3rem; font-weight: 800; color: #000000 !important; -webkit-text-fill-color: #000000 !important; margin-bottom: 0.25rem; letter-spacing: -0.02em;">
        The Standup & PR Polish Agent
    </div>
    <div style="font-size: 1.05rem; font-weight: 500; color: #1f2937 !important; -webkit-text-fill-color: #1f2937 !important; margin-bottom: 1.5rem; line-height: 1.5;">
        Transform raw, messy brain-dumps into crisp, confident daily standups and high-impact PR descriptions in milliseconds.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- MODE SELECTOR -----------------
col_mode, _ = st.columns([1, 2])
with col_mode:
    task_mode = st.radio(
        "Choose Mode",
        options=["Daily Standup 📋", "Pull Request Description 🔀"],
        horizontal=True,
        label_visibility="collapsed",
    )

task_type = "standup" if "Standup" in task_mode else "pr"

# ----------------- INPUT & CONTROLS -----------------
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

st.markdown("#### 📝 Raw Thoughts")

user_input = st.text_area(
    "Raw Input",
    value=st.session_state["input_text"],
    placeholder=(
        "Dump your unfiltered notes here...\n"
    ),
    height=160,
    label_visibility="collapsed",
)
st.session_state["input_text"] = user_input

# Action Buttons
btn_col1, btn_col2, _ = st.columns([2, 1, 4])
with btn_col1:
    transform_clicked = st.button("🚀 Transform", type="primary", use_container_width=True)
with btn_col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state["input_text"] = ""
        st.session_state.pop("polished_result", None)
        st.rerun()

# ----------------- INFERENCE & OUTPUT -----------------
if transform_clicked:
    clean_text = user_input.strip()
    if not clean_text or len(clean_text) < 5:
        st.error("Please enter at least a few words describing what you worked on!")
    else:
        with st.spinner("🤖 Transforming your notes into a professional update..."):
            result, err = call_polish_api(clean_text, task_type, base_url=backend_url)
            if err:
                st.error(err)
            elif result:
                st.session_state["polished_result"] = result

if "polished_result" in st.session_state:
    res = st.session_state["polished_result"]
    polished_text = res.get("polished_text", "")
    model_name = res.get("model_used", "gemini-2.5-flash")

    st.markdown("---")
    st.markdown(f"### 🎉 Polished Output ")

    tab_preview, tab_copy, tab_diff = st.tabs(["📄 Formatted Preview", "📋 One-Click Copy", "🔍 Before vs After"])

    with tab_preview:
        st.markdown(polished_text)

    with tab_copy:
        st.info("Click the copy icon on the top right of the code block below to copy to your clipboard:")
        st.code(polished_text, language="markdown")

    with tab_diff:
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown("**Original Raw Brain-dump:**")
            st.text_area("Original", value=user_input, height=200, disabled=True, label_visibility="collapsed")
        with d_col2:
            st.markdown("**Polished Output:**")
            st.text_area("Polished", value=polished_text, height=200, disabled=True, label_visibility="collapsed")
