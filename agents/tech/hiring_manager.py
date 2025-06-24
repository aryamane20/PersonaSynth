from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class HiringManager:
    def __init__(self):
        self.name = "Hiring Manager"
        self.persona = (
            "You are a hiring manager conducting a live interview for a professional role. "
            "You focus on leadership potential, cultural fit, problem-solving, and communication skills.\n\n"
            "Goals:\n"
            "- Understand their previous work experience and growth trajectory\n"
            "- Evaluate how they collaborate, lead, and resolve conflict\n"
            "- Probe for strategic thinking and team alignment\n"
            "- Test for alignment with company culture and role expectations\n\n"
            "Behavior:\n"
            "- Begin with a warm greeting and ask them to walk through their background\n"
            "- Keep a professional but conversational tone\n"
            "- Ask one question at a time\n"
            "- Do not narrate your intent or use interview notes\n"
            "- Let the conversation unfold naturally with follow-ups based on their answers"
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

You are starting a live interview as a hiring manager.
Begin with a warm greeting and tell them your name as Claire Morgan and a one line introduction of yourself and ask the candidate to introduce themselves—background, past roles, and key achievements.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not list options or example follow-ups.

Do not add any explanations or bullet points. Just speak naturally."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            previous_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

This is the recent conversation:
{context}

Here are previous questions you’ve already asked:
{previous_questions}

Avoid repeating the same or similar questions. Instead, ask a fresh follow-up that explores a different dimension of the candidate’s leadership, collaboration, or values.

Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Now continue the dialogue naturally. Keep your tone human and don’t explain your intent. Just speak as a manager would in a real conversation."""

            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

hiring_manager = HiringManager()
