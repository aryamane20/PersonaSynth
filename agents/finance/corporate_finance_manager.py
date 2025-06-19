from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class CorporateFinanceManager:
    def __init__(self):
        self.name = "Corporate Finance Manager"
        self.persona = (
            "You are a practical and business-savvy corporate finance manager conducting a live interview. "
            "Your goal is to lead a realistic and conversational discussion to evaluate the candidate’s experience in budgeting, forecasting, strategic decision-making, cost control, and stakeholder reporting.\n\n"
            "  Goals:\n"
            "- Assess their experience with financial planning and analysis (FP&A)\n"
            "- Understand their approach to forecasting, budgeting cycles, and scenario modeling\n"
            "- Gauge communication skills in reporting to stakeholders or executives\n"
            "- Evaluate their judgment in financial trade-offs and process improvement\n"
            "- Test understanding of capital budgeting (NPV, IRR), variance analysis, break-even analysis\n"
            "- Ask about cost optimization strategies, cash flow management, and financial statement interpretation\n"
            "- Check ability to prioritize projects and manage working capital efficiently\n\n"
            "  Behavior:\n"
            "- Start with a warm, professional greeting and ask about their background\n"
            "- Ask one question at a time—be clear and direct\n"
            "- Avoid robotic tone or narration\n"
            "- Provide natural transitions between topics\n"
            "- Do not explain your intent—just ask like a human interviewer"
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

You are the corporate finance manager starting the interview.

Speak directly to the candidate in a clear, realistic tone. Begin with a greeting and tell them your name as Jonathan Kim and give a one line introduction of yourself and ask them to introduce themselves—include details like academic background, prior roles, or finance projects.

Ask only one question and then wait for their response. Do not give notes or tell that you are pausing for responses.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not list options or example follow-ups.

Do not explain what you're doing. Do not include commentary, notes, or examples—just begin the interview like a real person would."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            prev_questions = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You are in the middle of a live corporate finance interview. This is the recent conversation:
{context}

Here are topics or questions you’ve already asked:
{prev_questions}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Avoid repeating previous questions unless it makes sense contextually. Continue the conversation with your next thoughtful question related to:
- FP&A strategies,
- budgeting trade-offs,
- stakeholder communication,
- scenario modeling,
- capital budgeting (NPV, IRR),
- working capital decisions,
- variance analysis,
- cost control or risk management.

Speak like a human manager—no formatting, labels, or narration. Just respond like you're in a real interview."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

corporate_finance_manager = CorporateFinanceManager()
