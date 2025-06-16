from langchain_community.chat_models import ChatOpenAI

class FeedbackEvaluator:
    def __init__(self):
        self.model = ChatOpenAI(
            api_key="sk-492256da50af4813b2d96c6be1909918",
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.3
        )

    def evaluate(self, transcript):
        prompt = f"""
You are an expert interview coach. Evaluate the following interview transcript.

For each of these categories:
- Communication
- Problem Solving
- Technical Knowledge
- Clarity of Thought
- Professionalism

Give a score from 0 to 10 and 1 sentence justification.

Then give a 3-4 sentence summary of the candidate's overall performance.

Transcript:
{transcript}

Return the output in this format:
Communication: [score], [comment]
Problem Solving: [score], [comment]
Technical Knowledge: [score], [comment]
Clarity of Thought: [score], [comment]
Professionalism: [score], [comment]
Summary: [summary text]
"""

        result = self.model.predict(prompt)

        feedback = {}
        for line in result.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if "," in value:
                    try:
                        score_str, comment = value.split(",", 1)
                        score = int(score_str.strip())
                        feedback[key] = (score, comment.strip())
                    except:
                        feedback[key] = value
                else:
                    feedback[key] = value

        return feedback


# Instantiate evaluator
evaluator = FeedbackEvaluator()
