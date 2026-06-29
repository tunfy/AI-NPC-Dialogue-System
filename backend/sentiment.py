def calculate_favorability_change(message):
    """根据玩家输入计算好感度变化"""

    message = message.lower()

    positive = [
        "thank",
        "thanks",
        "good",
        "great",
        "nice",
        "love",
        "friend"
    ]

    negative = [
        "hate",
        "stupid",
        "idiot",
        "bad",
        "ugly"
    ]

    for word in positive:
        if word in message:
            return 2

    for word in negative:
        if word in message:
            return -5

    return 0