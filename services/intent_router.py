# -----------------------------------
# Intent Categories
# -----------------------------------

VALID_INTENTS = {
    "recommendation",
    "clarification",
    "comparison",
    "off_topic",
    "prompt_injection"
}


# -----------------------------------
# Detect Prompt Injection
# -----------------------------------

def is_prompt_injection(query):

    query = query.lower()

    injection_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "system prompt",
        "reveal prompt",
        "bypass",
        "override"
    ]

    return any(
        pattern in query
        for pattern in injection_patterns
    )


# -----------------------------------
# Detect Off-topic Queries
# -----------------------------------

def is_off_topic(query):

    query = query.lower()

    off_topic_keywords = [
        "legal advice",
        "firing employees",
        "tax advice",
        "medical advice",
        "politics",
        "religion"
    ]

    return any(
        keyword in query
        for keyword in off_topic_keywords
    )


# -----------------------------------
# Detect Comparison Queries
# -----------------------------------

def is_comparison(query):

    query = query.lower()

    comparison_keywords = [
        "compare",
        "difference between",
        "vs",
        "versus"
    ]

    return any(
        keyword in query
        for keyword in comparison_keywords
    )


# -----------------------------------
# Detect Vague Queries
# -----------------------------------

def is_vague_query(query):

    query = query.lower().strip()

    vague_patterns = [
        "i need an assessment",
        "recommend assessment",
        "help me hire",
        "need a test",
        "assessment"
    ]

    # Very short query
    if len(query.split()) <= 2:
        return True

    return any(
        pattern == query
        for pattern in vague_patterns
    )


# -----------------------------------
# Main Intent Router
# -----------------------------------

def classify_intent(query):

    if is_prompt_injection(query):
        return "prompt_injection"

    if is_off_topic(query):
        return "off_topic"

    if is_comparison(query):
        return "comparison"

    if is_vague_query(query):
        return "clarification"

    return "recommendation"