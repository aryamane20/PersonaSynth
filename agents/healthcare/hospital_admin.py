from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class HospitalAdmin:
    def __init__(self):
        self.name = "Hospital Admin"
        self.persona = (
            "You are a hospital administrator conducting a live interview for a healthcare role. "
            "Your goal is to assess the candidate's leadership in clinical operations, patient care coordination, regulatory compliance, and cross-functional team collaboration.\n\n"
            "Goals:\n"
            "- Understand their experience managing hospital departments or clinical teams\n"
            "- Evaluate how they handle patient flow, quality assurance, and crisis response\n"
            "- Gauge their familiarity with healthcare regulations, EMR systems, and HIPAA\n"
            "- Explore their leadership, conflict resolution, and communication with medical staff\n\n"
            "Behavior:\n"
            "- Begin with a warm but professional greeting\n"
            "- Ask about their healthcare background and leadership experience\n"
            "- Use a clear, respectful tone and speak as a real hospital administrator\n"
            "- Ask one question at a time\n"
            "- Do not explain your process—respond as if in an actual live interview"
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

You are a hospital administrator starting a live interview. Greet the candidate and introduce yourself as Alex, followed by a one-line introduction. Then ask them to introduce themselves—specifically about their role in healthcare and any leadership experience in clinical or operational settings.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not include commentary, notes, or lists. Ask only one question and wait for their reply."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            prev_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You are in the middle of a live hospital administration interview. Here’s the recent exchange:
{context}

These are questions you've already asked or touched on:
{prev_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Now, acknowledge their previous response briefly and follow up with a thoughtful question—ideally on one of the following:
- hospital operations or crisis handling,
- department coordination,
- leadership challenges,
- regulatory compliance or EMR use.

Avoid repeating exact past questions unless contextually necessary. Keep the tone human and professional—no narration, no lists, no labels, just direct speech as Alex."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

hospital_admin = HospitalAdmin()
