def generate_resume_questions(skills):

    if not skills:
        return []

    questions = []

    for skill in skills[:5]:
        questions.append(f"You have worked with {skill}. Can you explain a project where you used it?")
        questions.append(f"What challenges did you face while using {skill}?")

    return questions