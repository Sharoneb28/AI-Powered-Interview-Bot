def adapt_difficulty(current_difficulty, performance):

    if performance == "strong":

        if current_difficulty == "easy":
            return "medium"

        if current_difficulty == "medium":
            return "hard"

        return "hard"

    elif performance == "weak":
        return "easy"

    return current_difficulty