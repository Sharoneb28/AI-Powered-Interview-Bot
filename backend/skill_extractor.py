SKILLS = [
    "python",
    "machine learning",
    "sql",
    "react",
    "javascript",
    "docker",
    "aws"
]


def extract_skills(resume_text):

    found = []

    for skill in SKILLS:
        if skill.lower() in resume_text.lower():
            found.append(skill)

    return found