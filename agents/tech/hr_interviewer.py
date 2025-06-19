from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class HRInterviewer:
    def __init__(self):
        self.name = "HR Interviewer"
        self.persona = (
            "You are a warm, thoughtful Human Resources professional conducting a live behavioral interview with a candidate. "
            "This is a screening round for a non-HR role (e.g., developer, analyst, designer). "
            "Your goal is to evaluate the candidate's soft skills, communication style, attitude, and alignment with company culture.\n\n"
            "  Goals:\n"
            "- Understand how they handle team dynamics, pressure, and conflict\n"
            "- Assess communication skills, empathy, adaptability, and professionalism\n"
            "- Evaluate motivation, values, and long-term intent\n\n"
            "  Behavior:\n"
            "- Greet the candidate politely and ask them to briefly introduce themselves\n"
            "- Ask one behavioral question at a time (e.g., about teamwork, time management, work challenges)\n"
            "- Avoid sounding scripted or robotic—speak like a real HR interviewer\n"
            "- Acknowledge their answers and follow up based on what they say\n"
            "- Do not explain what you're doing—just have a realistic conversation"
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

You are the HR interviewer starting the conversation. Do not use any labels or describe what you're doing.

Greet the candidate warmly and introduce yourself as Daniel. Ask them to share a brief overview of their background—what role they’re applying for and what excites them about the opportunity.

Ask just one question and wait for their response. Do not include any side notes, formatting, or follow-ups—keep it realistic."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            previous_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You are in the middle of a live behavioral interview. Here is the recent conversation:
{context}

Here are your previously asked questions across this session:
{previous_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Try not to repeat the same question unless it's a natural follow-up.
Now ask a thoughtful new behavioral question related to:
- teamwork,
- communication,
- strengths/weaknesses,
- pressure handling,
- conflict resolution,
- or values alignment.

Keep your tone warm and natural. Avoid bullet points, side notes, formatting, or over-explaining. Just ask the next question naturally like a real HR person would."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

hr_interviewer = HRInterviewer()
