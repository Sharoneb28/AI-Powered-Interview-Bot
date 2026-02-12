# score_engine.py
# Core logic to score a single interview answer
from resume.resume_parser import resume_alignment_score
from scoring.metrics import SCORING_WEIGHTS


def score_confidence(answer_text):
    """
    Confidence proxy based on answer length
    """
    word_count = len(answer_text.split())

    if word_count < 10:
        return 3
    elif word_count < 25:
        return 6
    else:
        return 8


def score_response_time(response_time):
    """
    Faster responses indicate confidence (heuristic)
    """
    if response_time <= 20:
        return 9
    elif response_time <= 40:
        return 7
    else:
        return 5


def score_relevance(answer_text, question_text):
    """
    Simple keyword overlap for relevance
    """
    answer_words = set(answer_text.lower().split())
    question_words = set(question_text.lower().split())

    overlap = answer_words.intersection(question_words)
    relevance_score = min(len(overlap), 10)

    return relevance_score


def calculate_total_score(scores):
    """
    Weighted total score
    """
    total = 0
    for metric, weight in SCORING_WEIGHTS.items():
        total += scores.get(metric, 0) * weight

    return round(total, 2)


def score_answer(answer_text, question_text, response_time, resume_skills=None):
    if resume_skills is None:
        resume_skills = []

    scores = {
        "relevance": score_relevance(answer_text, question_text),
        "confidence": score_confidence(answer_text),
        "response_time": score_response_time(response_time),
        "clarity": 6,
        "grammar": 6,
        "resume_alignment": resume_alignment_score(answer_text, resume_skills)
    }

    scores["total_score"] = calculate_total_score(scores)
    return scores

