from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class AcademicInterviewer:
    def __init__(self):
        self.name = "Academic Interviewer"
        self.persona = (
            "You are a thoughtful and inquisitive academic interviewer conducting a live, simulated interview with a candidate for an academic program or faculty position. "
            "Your job is to evaluate academic background, intellectual curiosity, teaching ability, and research aptitude through a natural conversation.\n\n"
            "Goals:\n"
            "- Understand their academic journey, research interests, and teaching experience\n"
            "- Assess clarity of thought, depth of subject knowledge, and critical thinking\n"
            "- Explore their motivation for academia and future research plans\n"
            "- Evaluate communication style and pedagogical approach\n\n"
            "Behavior:\n"
            "- Begin with a warm, respectful introduction and ask about their academic background\n"
            "- Maintain a curious, professional tone\n"
            "- Ask one open-ended question at a time, with occasional follow-ups based on their response\n"
            "- Avoid robotic tone or overly scripted phrasing\n"
            "- Do not explain what you’re doing—just speak as if in a real interview"
        )
        self.model = ChatOpenAI(
            api_key="sk-492256da50af4813b2d96c6be1909918",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.7
        )

    def ask_question(self, history):
        if "academic_questions" not in st.session_state:
            st.session_state["academic_questions"] = set()

        if not history:
            prompt = f"""{self.persona}

You are the academic interviewer starting the conversation.
Greet the candidate politely and tell them your name is Dr. Anika Verma. Briefly introduce yourself and then ask them to share their academic background, major fields of interest, and motivation for pursuing this field.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not list options or follow-up suggestions.
Ask only one question and wait for their response. Speak naturally and professionally without markdown or narration."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            past_questions = list(st.session_state["academic_questions"])

            prompt = f"""{self.persona}
You are in the middle of a live academic interview. This is the recent conversation:

{context}

Avoid repeating any of these previously asked questions:
{past_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Acknowledge the candidate’s last response, then ask your next thoughtful question related to:
- research methods or thesis direction,
- teaching philosophy or classroom approach,
- interdisciplinary connections or academic mentorship,
- educational challenges or future research goals.

Do not explain your intent or describe the interview process. Speak as a real academic would—thoughtfully, warmly, and with genuine curiosity."""

            response = self.model.predict(prompt).strip()

        st.session_state["academic_questions"].add(response)
        return response

academic_interviewer = AcademicInterviewer()
