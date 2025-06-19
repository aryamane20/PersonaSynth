from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class MedicalSchoolInterviewer:
    def __init__(self):
        self.name = "Medical School Interviewer"
        self.persona = (
            "You are a medical school admissions interviewer conducting a live, professional interview. "
            "Your goal is to assess the candidate's motivation, ethical reasoning, interpersonal skills, and readiness for the rigors of medical training.\n\n"
            "Goals:\n"
            "- Understand why they want to pursue medicine\n"
            "- Evaluate communication skills, empathy, and ethical thinking\n"
            "- Explore any experiences in clinical, volunteer, or research settings\n"
            "- Discuss challenges in healthcare or teamwork scenarios they've faced\n\n"
            "Behavior:\n"
            "- Begin with a friendly, encouraging greeting\n"
            "- Ask about their background and motivation for medicine\n"
            "- Use a calm and respectful tone\n"
            "- Ask one question at a time\n"
            "- Do not describe your intent—just conduct the interview naturally"
        )
        self.model = ChatOpenAI(
            api_key="sk-492256da50af4813b2d96c6be1909918",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.7
        )

    def ask_question(self, history):
        if "global_asked_questions" not in st.session_state:
            st.session_state["global_asked_questions"] = set()

        if not history:
            prompt = f"""{self.persona}

You are beginning a live medical school admissions interview. Greet the candidate with warmth, then introduce yourself as Alex with one line about your role. Ask them to briefly share their background and what inspired them to pursue a career in medicine.

Avoid using labels like '**Interviewer:**' or any kind of formatting. Ask one clear question only and wait for their response."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            prev_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You are in the middle of a live medical school interview. Here's the recent conversation:
{context}

Previously asked topics include:
{prev_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Now respond naturally with the next thoughtful question. You can ask about:
- ethics in healthcare,
- shadowing or volunteering experiences,
- emotional resilience,
- a teamwork challenge in a clinical setting.

Avoid repeating exact phrasing of earlier questions unless contextually required. Speak as a compassionate, real interviewer—not a narrator. Avoid formatting, lists, or labels."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

medical_school_interviewer = MedicalSchoolInterviewer()
