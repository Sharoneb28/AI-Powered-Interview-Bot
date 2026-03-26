from ai_engine import generate_ai_question
from performance_analyzer import analyze_performance
import random

def generate_question(context, performance, answer):

    # 🔥 AUTO performance (override frontend)
    performance = analyze_performance(answer)

    # -------- RESUME QUESTIONS --------
    if context.resume_questions:
        q = context.resume_questions.pop(0)
        context.add_question(q)

        return {
            "question": q,
            "domain": "resume",
            "difficulty": "resume"
        }

    # -------- ADAPT DIFFICULTY --------
    from difficulty_adapter import adapt_difficulty
    new_difficulty = adapt_difficulty(context.difficulty, performance)

    # -------- DOMAIN TOPIC --------
    TOPICS = {
        "Software": ["OOP", "API", "Database", "DSA", "System Design"],
        "Web": ["HTML", "CSS", "JavaScript", "Frontend", "Backend"],
        "AI": ["Machine Learning", "Neural Networks", "Data", "Models"]
    }

    topics = TOPICS.get(context.domain, ["General"])
    topic = random.choice(topics)

    # -------- FOLLOW-UP (if strong answer) --------
    if performance == "strong" and answer:
        question = generate_ai_question(context.domain, topic, new_difficulty, answer)
    else:
        question = generate_ai_question(context.domain, topic, new_difficulty)

    # -------- SAVE --------
    if question in context.asked_questions:
        return generate_question(context, performance, "skip")

    context.add_question(question)
    context.difficulty = new_difficulty

    return {
        "question": question,
        "domain": context.domain,
        "difficulty": new_difficulty
    }