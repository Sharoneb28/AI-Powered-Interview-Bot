import random

from question_bank import QUESTION_BANK
from difficulty_adapter import adapt_difficulty
from followup_logic import should_ask_followup


def generate_dynamic_question(domain, difficulty, previous_question, answer, asked_questions):

    templates = [
        "You mentioned {keyword}. Can you explain how it works in {domain} systems?",
        "How would you optimize a system that uses {keyword} in {domain}?",
        "What challenges might occur when implementing {keyword} in {domain}?",
        "Describe a real-world scenario where {keyword} is used in {domain}.",
        "What are the advantages of using {keyword} in {domain} development?"
    ]

    words = [w.lower() for w in answer.split()]

    ignore_words = [
        "the","a","an","is","are","was","were","i","we","it",
        "software","system","project","application","using"
    ]

    keywords = [w for w in words if w not in ignore_words]

    if keywords:
        keyword = random.choice(keywords)
    else:
        keyword = domain

    # try multiple times to avoid repetition
    for _ in range(5):

        template = random.choice(templates)

        question = template.format(keyword=keyword, domain=domain)

        if question not in asked_questions:
            return question

    return question


def generate_question(context, performance, answer):

    # STEP 1 — Resume questions first
    if context.resume_questions:

        question = context.resume_questions.pop(0)

        context.add_question(question)

        return {
            "question": question,
            "domain": context.domain,
            "difficulty": "resume",
            "is_follow_up": False
        }

    # STEP 2 — Difficulty adaptation
    new_difficulty = adapt_difficulty(context.difficulty, performance)

    previous_question = context.get_previous_question()

    try:

        print("Generating dynamic AI-style question...")

        question = generate_dynamic_question(
            context.domain,
            new_difficulty,
            previous_question,
            answer,
            context.asked_questions
        )

    except Exception as e:

        print("Generator error:", e)
        print("Using fallback question bank")

        questions = QUESTION_BANK[context.domain][new_difficulty]

        available = [
            q for q in questions if q not in context.asked_questions
        ]

        if not available:
            context.asked_questions.clear()
            available = questions

        question = random.choice(available)

    context.add_question(question)
    context.update_difficulty(new_difficulty)

    return {
        "question": question,
        "domain": context.domain,
        "difficulty": new_difficulty,
        "is_follow_up": should_ask_followup(performance)
    }