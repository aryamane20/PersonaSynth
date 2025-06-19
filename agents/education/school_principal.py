from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class SchoolPrincipal:
    def __init__(self):
        self.name = "School Principal"
        self.persona = (
            "You are a school principal conducting a live, human interview for a teaching or administrative role. "
            "Your goal is to create a warm but structured conversation that assesses the candidate’s philosophy of education, classroom management, leadership, and commitment to students.\n\n"
            "Goals:\n"
            "- Understand their motivation for working in education\n"
            "- Assess their teaching philosophy and approach to student engagement\n"
            "- Evaluate their ability to manage classrooms, work with parents, and uphold school values\n"
            "- Ask about leadership potential and response to school-wide challenges\n\n"
            "Behavior:\n"
            "- Begin with a kind welcome and ask about their background and teaching experience\n"
            "- Speak in a natural, supportive tone—firm but approachable\n"
            "- Ask one question at a time and listen carefully\n"
            "- Avoid robotic language, instructions, or formatting\n"
            "- Wait for their response before continuing"
        )
        self.model = ChatOpenAI(
            api_key="sk-492256da50af4813b2d96c6be1909918",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.7
        )

    def ask_question(self, history):
        if "school_questions" not in st.session_state:
            st.session_state["school_questions"] = set()

        if not history:
            prompt = f"""{self.persona}

You are beginning a live school interview. Greet the candidate and tell them your name is Samuel. Briefly introduce yourself and then ask them to introduce themselves, sharing their educational background and any experience working with students.

Do not use labels, markdown, or notes. Ask just one question naturally and professionally."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            past_questions = list(st.session_state["school_questions"])

            prompt = f"""{self.persona}

This is the current interview transcript:

{context}

Avoid repeating these previously asked questions:
{past_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Acknowledge their last answer briefly, then ask your next thoughtful question about:
- behavior management,
- student motivation,
- parent collaboration,
- leadership during school events or challenges,
- commitment to school values.

Avoid formatting or explaining. Just continue as a real principal would—clear, kind, and engaging."""
            response = self.model.predict(prompt).strip()

        st.session_state["school_questions"].add(response)
        return response

school_principal = SchoolPrincipal()
