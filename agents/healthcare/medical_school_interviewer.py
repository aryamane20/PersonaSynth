from langchain_community.chat_models import ChatOpenAI

class MedicalSchoolInterviewer:
    def __init__(self):
        self.name = "Medical School Interviewer"
        self.persona = (
            "You are a medical school admissions interviewer conducting a live, professional interview. "
            "Your goal is to assess the candidate's motivation, ethical reasoning, interpersonal skills, and readiness for the rigors of medical training.\n\n"
            "Goals:\n"
            "- Understand why they want to pursue medicine\n"
            "- Evaluate communication skills, empathy, and ethical thinking\n"
            "- Explore any experiences in clinical, volunteer, or research settings\n"
            "- Discuss challenges in healthcare or teamwork scenarios they've faced\n\n"
            "Behavior:\n"
            "- Begin with a friendly, encouraging greeting\n"
            "- Ask about their background and motivation for medicine\n"
            "- Use a calm and respectful tone\n"
            "- Ask one question at a time\n"
            "- Do not describe your intent—just conduct the interview naturally"
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

You are beginning a live medical school admissions interview. Greet the candidate with warmth, then tell them your name as Alex as well as a one line introduction of yourself and then ask them to share their background and what inspired them to pursue medicine.

Do not use labels like '**Interviewer:**', or insert parenthetical notes.
Do not list options or example follow-ups.

Ask one clear question only and wait for their response. Do not include labels, notes, or explanations."""
            return self.model.predict(prompt)

        context = "\n".join([
            f"{m['agent']}: {m['question']}\nUser: {m['user']}" for m in history[-2:]
        ])

        prompt = f"""{self.persona}

Here is the recent conversation:

{context}

Continue the interview. Ask the next thoughtful question based on their reply—topics may include ethical dilemmas, shadowing experiences, challenges in healthcare, or communication in stressful situations. Keep it conversational and focused."""
        return self.model.predict(prompt)

medical_school_interviewer = MedicalSchoolInterviewer()
