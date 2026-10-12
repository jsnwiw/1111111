import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Satisfaction Dashboard", layout="wide")


# --- CSS: Glassmorphism and Animation Effects ---
st.markdown(
    """
    <style>
    /* Full Background */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
        background-attachment: fixed;
    }

    /* Animation Definition */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Sidebar Glass Style */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Main Card Style (Glassmorphism) */
    .stMetric, .stDataFrame, .stAlert, div.stButton > button {
        animation: fadeInUp 0.8s ease-out;
    }

    /* Custom Button Style */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.3);
        color: #1c1c1c;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        font-weight: bold;
        width: 100%;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.5);
        transform: scale(1.02);
        border: 1px solid #ffffff;
    }

    /* Input & Slider Style */
    .stTextInput input, .stSlider {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    /* Title Animation and Typography */
    h1 {
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Alert Box Glass Effect */
    .element-container div.stAlert {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Main Title
st.title("✨ Student Satisfaction Dashboard")
st.markdown("##### The student satisfaction survey is currently active. Please review the data below.")


# Initialize Session State
if "responses" not in st.session_state:
    st.session_state.responses = []


# Sidebar Input Section
st.sidebar.header("📝 Input Section")
student_name = st.sidebar.text_input(
    "Student Name", value="", placeholder="Enter name"
)
st.sidebar.markdown("---")
st.sidebar.header("📊 Satisfaction")
score = st.sidebar.slider(
    "Satisfaction Score", min_value=0, max_value=100, value=50, step=1
)
submit_button = st.sidebar.button("🚀 Submit Data")
view_button = st.sidebar.button("📂 View Saved Responses")


col1, col2 = st.columns([1, 1])


if submit_button:
    with st.spinner("Processing data securely..."):
        progress_bar = st.progress(0)
        for progress in range(1, 101):
            time.sleep(0.01)
            progress_bar.progress(progress)

    # Data validation and storage
    raw_scores = [score]
    clipped_scores = np.clip(raw_scores, 0, 100)
    final_score = int(clipped_scores[0])
    name_to_save = student_name.strip() or "Anonymous Student"

    st.session_state.responses.append({
        "Student Name": name_to_save,
        "Satisfaction Score": final_score,
        "Timestamp": time.strftime("%H:%M:%S"),
    })

    with col1:
        st.markdown("### Result")
        if final_score >= 80:
            st.success(f"🌟 **Highly Satisfied!** ({final_score} pts)")
        elif final_score >= 50:
            st.info(f"😊 **Satisfied / Above Average!** ({final_score} pts)")
        else:
            st.warning(f"⚠️ **Needs Improvement..** ({final_score} pts)")


# View Saved Responses Logic
if view_button:
    with col2:
        st.subheader("📋 Saved Responses")
        if st.session_state.responses:
            df_responses = pd.DataFrame(st.session_state.responses)
            # Dataframe styling
            st.dataframe(
                df_responses.style.highlight_max(
                    axis=0, subset=["Satisfaction Score"], color="#d4edda"
                ),
                use_container_width=True,
            )
        else:
            st.info(
                "No responses saved yet. Please submit the first response!"
            )