def analyze_performance(answer):

    if not answer or len(answer.strip()) < 10:
        return "weak"

    if len(answer.split()) > 25:
        return "strong"

    return "average"