def generate_resume_questions(skills):

    questions = []

    for skill in skills:

        questions.append(
            f"Explain a project where you used {skill}."
        )

        questions.append(
            f"What challenges did you face while working with {skill}?"
        )

    return questions