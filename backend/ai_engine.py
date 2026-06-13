def calculate_priority(quantity, expiry_hours):

    score = 0

    # More food = higher priority
    score += quantity * 0.3

    # Less time remaining = higher priority
    score += (24 - expiry_hours) * 3

    if score > 100:
        score = 100

    return int(score)