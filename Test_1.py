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

# === Mode Selection ===
mode = st.radio("Choose Interview Mode", ["🧠 Predefined Agent", "🛠️ Build Your Own"])

if mode == "🧠 Predefined Agent":
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
            selected_agent = st.selectbox("Interviewer", options=agent_options)

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

elif mode == "🛠️ Build Your Own":
    with st.form("custom_interviewer_form"):
        role = st.text_input("What role is the interviewer simulating?")
        traits = st.multiselect("Personality traits", ["Friendly", "Skeptical", "Technical", "Casual", "Demanding", "Curious"])
        domains = st.multiselect("Evaluation Areas", ["Problem Solving", "Technical Depth", "Communication", "Leadership", "Finance", "System Design"])
        question_types = st.multiselect("Question Types", ["Behavioral", "Technical", "Situational", "Case-based"])
        submitted = st.form_submit_button("Generate Interviewer")

    if submitted and role:
        traits_str = ", ".join(traits)
        domains_str = ", ".join(domains)
        qtypes_str = ", ".join(question_types)

        persona_prompt = f"""
        You are a {role} conducting a live, simulated interview.
        Your personality is {traits_str.lower()}.
        Focus on the following areas: {domains_str.lower()}.
        Ask {qtypes_str.lower()} questions, one at a time.
        Keep the conversation fluid, professional, and natural—respond like a real human interviewer.
        Do not use markdown, labels, or narration—just speak directly to the candidate.
        """

        from langchain_community.chat_models import ChatOpenAI

        class CustomInterviewer:
            def __init__(self, name, persona):
                self.name = name
                self.persona = persona
                self.model = ChatOpenAI(
                    api_key="sk-492256da50af4813b2d96c6be1909918",
                    base_url="https://api.deepseek.com/v1",
                    model="deepseek-chat",
                    temperature=0.7
                )

            def ask_question(self, history):
                if not history:
                    prompt = f"""{self.persona}

Begin with a brief greeting and ask the candidate to introduce themselves."""
                    return self.model.predict(prompt)
                context = "\n".join([f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]])
                prompt = f"""{self.persona}

This is the recent conversation:
{context}

Now continue the interview by asking the next thoughtful question in a realistic tone. Ask only one question at a time."""
                return self.model.predict(prompt)

        agent = CustomInterviewer(role, persona_prompt)

# === Rest of the app remains the same and uses the selected `agent` instance ===
