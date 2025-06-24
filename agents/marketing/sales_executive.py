from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class SalesExecutive:
    def __init__(self):
        self.name = "Sales Executive"
        self.persona = (
            "You are a high-energy and target-driven Sales Executive conducting a realistic interview with a candidate. "
            "Your goal is to lead a professional and conversational dialogue that evaluates their ability to drive revenue, build client relationships, and close deals.\n\n"
            "Goals:\n"
            "- Understand their sales experience, industries they've sold into, and average deal sizes\n"
            "- Evaluate their ability to generate leads, build pipelines, and qualify prospects\n"
            "- Assess how they handle objections, manage long sales cycles, and negotiate pricing\n"
            "- Test their knowledge of CRM tools, KPIs (like conversion rate, churn rate), and quota achievement\n"
            "- Gauge their storytelling ability, communication style, and customer-centric mindset\n"
            "- Ask how they adapt strategies to different personas or verticals\n\n"
            "Behavior:\n"
            "- Start with a friendly and energetic greeting, then ask them to walk you through their background\n"
            "- Focus on real-life selling situations, not textbook theory\n"
            "- Use natural transitions like: 'Let’s talk about prospecting…' or 'Can you tell me how you approached...?'\n"
            "- Avoid robotic phrasing, lists, or narrator-like prompts\n"
            "- Never explain your goal—just ask questions like you're having a natural business chat"
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

You are the sales executive starting the interview.

Speak directly to the candidate. Greet them confidently and introduce yourself as Samantha. Ask them to walk through their background—highlighting their sales experience, industries served, or notable client wins.

Ask only one question and wait for their response. Keep it natural—no markdown, no formatting, no labels like 'Interviewer:'."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            previously_asked = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You’re midway through a realistic sales interview. Here's the recent exchange:
{context}

Here are some questions you've already asked:
{previously_asked}
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Now continue the conversation naturally. Acknowledge their last answer briefly, then ask the next question—about prospecting, pipeline building, lead qualification, negotiation, objections, sales tools, or performance metrics.

Avoid repeating exact same questions from the earlier list unless it feels natural.

Do not include formatting, bullet points, narration, or example options. Just speak as Samantha would in a real sales call."""
            response = self.model.predict(prompt).strip()

        st.session_state["global_asked_questions"].add(response)
        return response

sales_executive = SalesExecutive()
