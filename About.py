import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="PersonaSynth | Interview Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
    <style>
     section[data-testid="stSidebar"] {
        background-color: #15803d; 
        color: #14532d;
    }
    section[data-testid="stSidebar"] .css-1d391kg {
        color: black
        font-weight: bold;
    }
    body {
        background-color: #f8f9fc;
    }
    .hero-text {
        text-align: left;
        width: auto;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #14532d;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #4d4d4d;
        margin-top: 10px;
        margin-bottom:20px;
    }

    .button-wrapper {
        display: flex;
        justify-content: center;
    }
    .green-btn {
        background-color: #15803d;
        color: white;
        font-size: 18px;
        padding: 12px 36px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .green-btn:hover {
        background-color: #14532d;
    }
    .section-title {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 10px;
        color: #14532d;
    }
    .feature-row {
        display: flex;
        align-items:center;
        justify-content: center;
        flex-wrap: wrap;
    }
    .feature-box {
        background-color: #15803d;
        border-radius: 12px;
        color: white;
        padding: 24px;
        width: 800px;
        margin: 2px 100px 12px 275px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    .feature-box:hover {
        background-color: #14532d;
    }
    .logo-container {
        margin-bottom:10px;
    }
    .step-container {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex-wrap: wrap;
    }
    .step-box {
        text-align: center;
        width: 800px;
        margin: 2px 100px 12px 275px;
    }
    .step-circle {
        background-color: #15803d;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        margin: 0 auto 6px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Text + Logo ---
logo = Image.open("PSlogo.jpeg") 
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <img src="data:image/png;base64,{logo_b64}" width="250" class="logo-container" />
        <div class="hero-text" style="max-width: 700px; margin: 0 auto; text-align: left;">
            <div class="hero-title">Prepare Smarter, Interview Better</div>
            <div class="hero-subtitle">
                Whether you're preparing for your first job interview or aiming to level up your career, PersonaSynth empowers you to practice with lifelike AI personas tailored to your industry and role. Our adaptive interview engine provides personalized questions, real-time feedback, and actionable insights—so you can walk into every interview with confidence and clarity.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- Button ---
st.markdown("""
    <div class="button-wrapper">
         <a href="?nav=InterviewSimulator">
            <button class="green-btn" type="submit">
               Start Your Prep!
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

if st.query_params.get("nav") == "InterviewSimulator":
    st.switch_page("pages/InterviewSimulator.py")

st.markdown('<div class="section-title">Why Choose PersonaSynth?</div>', unsafe_allow_html=True)
st.markdown('<div class="feature-row">', unsafe_allow_html=True)

features = [
    ("Smart Question Bank", "Thousands of role-specific questions tailored to your industry and level."),
    ("AI Mock Interviews", "Realistic simulations with adaptive AI-driven agents."),
    ("Answer Templates", "Use proven response frameworks to structure your answers.")
]

for icon, text in features:
    st.markdown(f'<div class="feature-box"><strong>{icon}</strong><br>{text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">How It Works?</div>', unsafe_allow_html=True)
st.markdown('<div class="step-container">', unsafe_allow_html=True)

steps = [
    ("1", "Select a Persona", "Choose your interviewer – recruiter, manager, or expert."),
    ("2", "Practice Interviews", "Respond to adaptive questions in real time."),
    ("3", "Get Feedback", "Review your performance and improve confidently.")
]

for num, title, desc in steps:
    st.markdown(f"""
        <div class="step-box">
            <div class="step-circle">{num}</div>
            <strong>{title}</strong><br>
            <div>{desc}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <hr style="margin-top: 20px; margin-bottom: 0;"/>
    <div style='text-align: right; font-size: 0.9em; color: black; padding-right: 20px;'>
        © Developed by Arya Mane and Ameya Phansalkar
    </div>
""", unsafe_allow_html=True)
