import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# === Page Config ===
st.set_page_config(
    page_title="PersonaForge | AI Interview Simulator",
    page_icon="💬",
    layout="centered"
)

# === Branding Header ===
st.markdown("""
<style>
h1 {
    font-size: 42px;
    text-align: center;
    margin-top: 40px;
}
.subtitle {
    font-size: 20px;
    text-align: center;
    color: #555;
    margin-bottom: 40px;
}
.feature-box {
    background-color: #f8f9fa;
    padding: 24px;
    margin: 12px 0;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.05);
}
</style>

<h1>PersonaForge 💬</h1>
<div class="subtitle">Simulate real interviews with AI-driven personas across industries.</div>
""", unsafe_allow_html=True)

# === Features Section ===
st.markdown("""
<div class="feature-box">
    <strong>🎭 Hyper-Realistic Interview Personas</strong><br>
    Choose from technical recruiters, hiring managers, or domain-specific professionals like IB Analysts or Medical School Interviewers.
</div>
<div class="feature-box">
    <strong>🧠 Intelligent Dialogue</strong><br>
    Experience adaptive conversations with questions that evolve based on your answers.
</div>
<div class="feature-box">
    <strong>📊 Feedback & Performance Scoring</strong><br>
    Get detailed feedback with scores on communication, clarity, domain knowledge, and more.
</div>
<div class="feature-box">
    <strong>📂 Industry-Tailored Simulation</strong><br>
    Practice interviews in tech, finance, healthcare, education, and more.
</div>
""", unsafe_allow_html=True)

# === Call-to-Action Button ===
if st.button("🎯 Enter Interview Mode"):
    switch_page("main2")
