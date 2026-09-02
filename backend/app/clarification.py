import re


def detect_ambiguity(question: str):
    """
    Detect whether a user's question may be ambiguous
    and require clarification before SQL generation.
    """

    question_lower = question.lower().strip()

    # Empty question
    if not question_lower:
        return {
            "needs_clarification": True,
            "clarification_question": "What would you like to know from the database?"
        }

    # Very short questions are often incomplete
    if len(question_lower.split()) < 3:
        return {
            "needs_clarification": True,
            "clarification_question": "Could you provide more details about what you would like to find?"
        }

    # Ambiguous words that can have multiple meanings
    ambiguous_words = {
        "best": "What do you mean by 'best'?",
        "top": "What do you mean by 'top'?",
        "highest": "What should be the highest value based on?",
        "lowest": "What should be the lowest value based on?",
        "most": "What should be the highest value based on?",
        "least": "What should be the lowest value based on?",
        "good": "What do you mean by 'good'?",
        "recent": "What time period should be considered recent?",
        "old": "Do you mean the oldest by age, date, or something else?",
        "young": "Do you mean the youngest by age or something else?"
    }

    for word, clarification in ambiguous_words.items():
        pattern = rf"\b{re.escape(word)}\b"

        if re.search(pattern, question_lower):
            return {
                "needs_clarification": True,
                "clarification_question": clarification
            }

    # Detect questions where an important comparison value is missing
    if re.search(r"\bshow me the (student|students|teacher|teachers|course|courses)\b", question_lower):
        if any(word in question_lower for word in ["best", "top", "highest", "lowest"]):
            return {
                "needs_clarification": True,
                "clarification_question": "What criteria should I use to determine the result?"
            }

    return {
        "needs_clarification": False,
        "clarification_question": None
    }