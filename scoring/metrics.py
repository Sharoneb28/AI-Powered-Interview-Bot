# metrics.py
# Defines scoring weights and thresholds

SCORING_WEIGHTS = {
    "relevance": 0.30,
    "clarity": 0.25,
    "grammar": 0.20,
    "confidence": 0.15,
    "response_time": 0.10
}

PERFORMANCE_LEVELS = {
    "Beginner": (0, 4),
    "Intermediate": (4, 7),
    "Advanced": (7, 10)
}
