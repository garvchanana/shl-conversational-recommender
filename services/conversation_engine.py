# -----------------------------------
# Clarification Question
# -----------------------------------

def generate_clarification():

    return (
        "Could you share:\n"
        "- the role you are hiring for,\n"
        "- seniority level,\n"
        "- and whether technical, cognitive, "
        "or personality assessments are needed?"
    )


# -----------------------------------
# Off-topic Refusal
# -----------------------------------

def off_topic_response():

    return (
        "I can only assist with SHL assessment "
        "recommendations and comparisons."
    )


# -----------------------------------
# Prompt Injection Refusal
# -----------------------------------

def injection_response():

    return (
        "I can only operate within SHL "
        "assessment recommendation guidelines."
    )

# -----------------------------------
# Refinement Detection
# -----------------------------------

def is_refinement_query(query):

    query = query.lower()

    refinement_keywords = [
        "also",
        "add",
        "include",
        "actually",
        "in addition",
        "along with"
    ]

    return any(
        keyword in query
        for keyword in refinement_keywords
    )


# -----------------------------------
# Build Conversation Context
# -----------------------------------

def build_conversation_context(messages):

    """
    Reconstruct conversational context
    from stateless message history.
    """

    user_messages = [
        msg.content
        for msg in messages
        if msg.role == "user"
    ]

    combined_context = " ".join(user_messages)

    return combined_context