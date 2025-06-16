import streamlit as st
import importlib
import time

# === UI Setup ===
st.set_page_config(
    page_title="PersonaForge",
    page_icon="💬",
    layout="centered"
)
st.title("PersonaForge")
st.caption("Interview Simulation")

# === Define industry → agents → subroles structure ===
INDUSTRY_AGENTS = {
    "Tech & Software": {
        "Hiring Manager": "agents.tech.hiring_manager",
        "HR Interviewer": "agents.tech.hr_interviewer",
        "Technical Recruiter": {
            "Python": "agents.tech.technical_recruiter",
            "Java": "agents.tech.technical_recruiter",
            "SQL": "agents.tech.technical_recruiter",
            "C++": "agents.tech.technical_recruiter"
        }
    },
    "Finance": {
        "IB Analyst": "agents.finance.ib_analyst",
        "Financial Advisor": "agents.finance.financial_advisor",
        "Corporate Finance Manager": "agents.finance.corporate_finance_manager"
    },
    "Marketing & Sales": {
        "Sales Executive": "agents.marketing.sales_executive",
        "Brand Manager": "agents.marketing.brand_manager"
    },
    "Healthcare": {
        "Medical School Interviewer": "agents.healthcare.medical_school_interviewer",
        "Hospital Admin": "agents.healthcare.hospital_admin"
    },
    "Education": {
        "Academic Interviewer": "agents.education.academic_interviewer",
        "School Principal": "agents.education.school_principal"
    }
}

# === Session State Setup ===
for key, val in {
    "history": [], "current_prompt": None, "current_agent": None,
    "turn": 0, "started": False, "feedback": None, "active_key": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# === Constants ===
MAX_TURNS = 6

# === Step 1: Industry and Agent Selection ===
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        industry = st.selectbox(
            "Industry",
            options=list(INDUSTRY_AGENTS.keys()),
            format_func=lambda x: {
                "Tech & Software": "Technology",
                "Finance": "Finance",
                "Marketing & Sales": "Marketing & Sales",
                "Healthcare": "Healthcare",
                "Education": "Education"
            }.get(x, str(x))
        )
    agents = INDUSTRY_AGENTS[industry]

    with col2:
        agent_options = list(agents.keys())
        selected_agent = st.selectbox(
            "Interviewer",
            options=agent_options,
            format_func=lambda x: str(x)
        )

# === Agent Loading ===
if isinstance(agents[selected_agent], dict):
    subroles = list(agents[selected_agent].keys())
    selected_subrole = st.selectbox("Select Specialization", subroles)
    module_path = agents[selected_agent][selected_subrole]
    agent_module = importlib.import_module(module_path)
    agent = agent_module.TechnicalRecruiter(language=selected_subrole)
else:
    module_path = agents[selected_agent]
    agent_module = importlib.import_module(module_path)
    agent = getattr(agent_module, module_path.split('.')[-1])

# === Reset session state on agent change ===
new_key = f"{industry}-{selected_agent}-{selected_subrole if 'selected_subrole' in locals() else ''}"
if st.session_state.active_key != new_key:
    st.session_state.active_key = new_key
    for key in ["history", "current_prompt", "current_agent", "turn", "started", "feedback"]:
        st.session_state[key] = [] if key == "history" else 0 if key == "turn" else None if key == "feedback" else False

# === Start Interview Button ===
if not st.session_state.started:
    if st.button("Start Interview"):
        st.session_state.started = True
        first_q = agent.ask_question([])
        st.session_state.history.append({
            "agent": agent.name,
            "question": first_q,
            "user": ""
        })

# === Chat Interface ===
if st.session_state.started:

    def chat_bubble(content, sender, color, align_right=False):
        tail = f"""
            content: \"\";
            position: absolute;
            top: 12px;
            {'left' if not align_right else 'right'}: -12px;
            width: 0;
            height: 0;
            border: 8px solid transparent;
            border-{'right' if not align_right else 'left'}-color: {color};
        """
        align = "margin-left: auto;" if align_right else "margin-right: auto;"
        return f"""
            <div style='{align} max-width: 70%; display: flex; flex-direction: column;'>
                <div style='position: relative; padding: 12px 14px; margin:8px 8px 12px 8px; border-radius: 16px; background-color: {color}; color: white; font-size: 15px; font-weight: 400;'>
                    <strong>{sender}:</strong><br>{content}
                    <div style='{tail}'></div>
                </div>
            </div>
        """

    agent_color = "#0077b6"
    user_color = "#444444"

    current_round = len([m for m in st.session_state.history if m['user']]) + 1
    st.markdown(f"### Round {min(current_round, MAX_TURNS)} of {MAX_TURNS}")
    st.progress(min(current_round, MAX_TURNS) / MAX_TURNS)

    for turn in st.session_state.history:
        if turn["question"]:
            st.markdown(chat_bubble(turn["question"], turn["agent"], agent_color, align_right=False), unsafe_allow_html=True)
        if turn["user"]:
            st.markdown(chat_bubble(turn["user"], "🧑 You", user_color, align_right=True), unsafe_allow_html=True)

    if len(st.session_state.history) < MAX_TURNS:
        user_input = st.chat_input("Your response")
        if user_input:
            st.session_state.history[-1]["user"] = user_input
            st.markdown(chat_bubble(user_input, "🧑 You", user_color, align_right=True), unsafe_allow_html=True)
            with st.spinner("Agent is typing..."):
                time.sleep(1.0)
            new_q = agent.ask_question(st.session_state.history)
            st.session_state.history.append({
                "agent": agent.name,
                "question": new_q,
                "user": ""
            })
            st.rerun()

    elif len(st.session_state.history) >= MAX_TURNS:
        st.success("Interview Complete!")

        if st.session_state.feedback is None:
            if st.button("Get Feedback Summary"):
                from feedback_evaluator import evaluator
                full_transcript = "\n".join(
                    [f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in st.session_state.history]
                )
                with st.spinner("Evaluating your performance..."):
                    st.session_state.feedback = evaluator.evaluate(full_transcript)

        if isinstance(st.session_state.feedback, dict):
            st.markdown("### 🧠 Interview Feedback")
            for skill, value in st.session_state.feedback.items():
                if skill == "Summary":
                    continue
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    score, comment = value
                    st.markdown(f"**{skill}** – {comment}")
                    st.markdown(f"""
<div style='margin-bottom: 16px;'>
  <div style='display: flex; justify-content: space-between;'>
    <strong>{skill}</strong>
    <span style='font-size: 14px;'>Score: {score}/10</span>
  </div>
  <div style='height: 14px; background-color: #ddd; border-radius: 6px;'>
    <div style='height: 100%; width: {score * 10}%; background-color: {'#e63946' if score < 5 else '#2a9d8f'}; border-radius: 6px; transition: width 0.4s ease-in-out;'></div>
  </div>
  <div style='margin-top: 6px; font-size: 13px;'>{comment}</div>
</div>
""", unsafe_allow_html=True)
            st.markdown("### 🗾 Summary")
            st.info(st.session_state.feedback.get("Summary", "No summary available."))

        elif st.session_state.feedback:
            st.markdown("### Interview Feedback")
            st.markdown(st.session_state.feedback)

        if st.button("🔄 Restart Interview", help="Click to start over"):
            for key in ["history", "current_prompt", "current_agent", "turn", "started", "feedback"]:
                st.session_state[key] = [] if key == "history" else 0 if key == "turn" else None if key == "feedback" else False