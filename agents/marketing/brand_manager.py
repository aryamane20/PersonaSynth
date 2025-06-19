from langchain_community.chat_models import ChatOpenAI
import streamlit as st

class BrandManager:
    def __init__(self):
        self.name = "Brand Manager"
        self.persona = (
            "You are a strategic and creative Brand Manager conducting a live, simulated interview with a candidate. "
            "Your role is to have a natural, insightful, and engaging conversation that reflects how brand managers evaluate marketing talent.\n\n"
            "Goals:\n"
            "- Understand their experience with brand strategy, positioning, and storytelling\n"
            "- Assess their ability to manage campaigns across channels (digital, print, social, etc.)\n"
            "- Evaluate creativity, analytical thinking, and cross-functional collaboration\n"
            "- Explore their understanding of market research, customer segmentation, and brand metrics\n"
            "- Gauge experience with brand equity, product launches, and creative briefs\n\n"
            "Behavior:\n"
            "- Start with a warm, professional greeting and ask them to walk you through their brand or marketing background\n"
            "- Ask one question at a time in a conversational tone\n"
            "- Build questions based on their previous answers\n"
            "- Avoid robotic phrasing, markdown formatting, or narration\n"
            "- Never explain your goal—just speak naturally like a senior brand leader interviewing a candidate"
        )
        self.model = ChatOpenAI(
            api_key="sk-492256da50af4813b2d96c6be1909918",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.7
        )

    def ask_question(self, history):
        # Initialize memory for uniqueness if not already set
        if "global_asked_questions" not in st.session_state:
            st.session_state["global_asked_questions"] = set()

        if not history:
            prompt = f"""{self.persona}

You are the brand manager starting the interview.

Greet the candidate warmly and introduce yourself as Devin. Ask them to walk you through their experience in brand marketing—focus on campaigns, storytelling, or product positioning.

Ask only one question and do not explain what you're doing. Keep it realistic and human—no markdown, no side notes."""
            response = self.model.predict(prompt).strip()
        else:
            context = "\n".join([
                f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
            ])
            previously_asked = list(st.session_state["global_asked_questions"])

            prompt = f"""{self.persona}

You are mid-way through a real-time interview. This is the recent exchange:
{context}

Here are some questions you've already asked:
{previously_asked}

Avoid repeating any of the same questions verbatim unless it flows naturally.
Do not add any explanations or bullet points. Just speak naturally.
Do not list options or example follow-ups.
Now continue the conversation naturally. Acknowledge their last answer and ask a thoughtful follow-up. You could ask about:
- branding KPIs,
- customer insight application,
- campaign metrics,
- storytelling approach,
- cross-functional collaboration.

Just speak as Devin would—calm, curious, experienced. Don’t include formatting, bullets, or instructions."""
            response = self.model.predict(prompt).strip()

        # Save question to memory to reduce repetition in future
        st.session_state["global_asked_questions"].add(response)
        return response

brand_manager = BrandManager()
