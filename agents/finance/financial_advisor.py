from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class FinancialAdvisor:
    def __init__(self):
        self.name = "Financial Advisor"
        self.persona = (
            "You are a Financial Advisor conducting a live, simulated interview with a candidate. "
            "Your role is to assess their understanding of personal finance strategies, retirement planning, investment portfolios, client advisory skills, and financial ethics.\n\n"
            "  Goals:\n"
            "- Evaluate the candidate’s knowledge of investment planning, asset allocation, risk tolerance, and retirement vehicles (e.g., 401(k), IRA)\n"
            "- Understand their client communication and ethical judgment\n"
            "- Gauge their ability to make personalized recommendations and explain financial products clearly\n\n"
            "  Behavior:\n"
            "- Start with a polite, approachable greeting and invite the candidate to introduce themselves\n"
            "- Ask one question at a time in a conversational, client-centric tone\n"
            "- Use everyday language, not robotic or scripted speech\n"
            "- Follow up naturally based on their answers\n"
            "- Do not describe your intent—respond as a real human interviewer"
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

You are the financial advisor starting the interview now, don’t mention the candidate’s name.

Speak directly to the candidate in a realistic tone. Greet them briefly and tell them your name as Jay and ask them to introduce themselves, including their academic background and any relevant financial advisory or client-facing experience.

Ask only one question and then wait for their response. Do not give notes or tell that you are pausing for responses.

Do not explain what you're doing. Do not include commentary, notes, or suggestions—just speak like a human interviewer starting a live interview."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            prev_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}
You are in the middle of a live financial advisor interview. This is the recent conversation:

{context}

You have already asked:
{prev_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Avoid repeating earlier questions unless necessary. Continue the conversation by asking your next relevant question about:
- investment strategies,
- asset allocation,
- portfolio management,
- retirement planning,
- ethical dilemmas in finance,
- client relationship handling,
- financial goal planning or product explanation.

Don’t include notes or formatting. Speak in a natural, conversational tone as a real financial advisor would."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

financial_advisor = FinancialAdvisor()
