class ConversationContext:

    def __init__(self, domain, resume_questions=None):
        self.domain = domain
        self.difficulty = "easy"
        self.asked_questions = set()
        self.resume_questions = resume_questions or []
        self.last_topic = None   # 🔥 important

    def add_question(self, q):
        self.asked_questions.add(q)