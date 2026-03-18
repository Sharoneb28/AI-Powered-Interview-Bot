class ConversationContext:

    def __init__(self, domain, resume_questions=None):
        self.domain = domain
        self.difficulty = "easy"
        self.asked_questions = []
        self.resume_questions = resume_questions or []

    def add_question(self, question):
        if question not in self.asked_questions:
            self.asked_questions.append(question)

    def update_difficulty(self, difficulty):
        self.difficulty = difficulty

    def get_previous_question(self):
        if self.asked_questions:
            return self.asked_questions[-1]
        return None