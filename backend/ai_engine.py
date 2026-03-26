import random

def generate_ai_question(domain, topic, difficulty, answer=None):

    if answer:
        # 🔥 FOLLOW-UP QUESTION
        return f"You mentioned '{answer[:30]}...'. Can you explain it in more detail?"

    if difficulty == "easy":
        return f"Can you explain the basic concept of {topic} in {domain}?"

    elif difficulty == "medium":
        return f"How would you apply {topic} in a real-world {domain} project?"

    else:
        return f"What are the challenges and optimization techniques in {topic}?"