from langchain_community.chat_models import ChatOpenAI

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
        if not history:
            prompt = f"""{self.persona}

You are a hospital administrator starting a live interview. Greet the candidate and them your name as Alex as well as a one line introduction of yourself and then ask them to introduce themselves. ask them to introduce themselves. Ask about their role in healthcare and leadership in any clinical or operational capacity.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not list options or example follow-ups.

Do not include commentary, notes, or labels. Ask only one question and wait for their reply."""
            return self.model.predict(prompt)

        context = "\n".join([
            f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
        ])

        prompt = f"""{self.persona}

Here is the recent conversation:

{context}

Now, follow up based on what they shared. Ask your next realistic question about operations management, interdepartmental coordination, crisis handling, or healthcare compliance. Stay conversational and focused on real-world hospital challenges."""
        return self.model.predict(prompt)

hospital_admin = HospitalAdmin()
