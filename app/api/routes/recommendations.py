def score_destination(user_preferences: dict, destination: dict):
    score = 0
    for category, weight in user_preferences.items():
        if category in destination["tags"]:
            score += weight

    return round(score, 2)