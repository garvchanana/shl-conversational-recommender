from services.retriever import retrieve_assessments
from services.groq_service import generate_response


# -----------------------------------
# Clean Response
# -----------------------------------

def clean_response(text):

    if not text:
        return ""

    return " ".join(text.split())

# -----------------------------------
# Personality Detection
# -----------------------------------

def requires_personality(query):

    query = query.lower()

    personality_keywords = [
        "personality",
        "behavioral",
        "behavior",
        "culture fit"
    ]

    return any(
        keyword in query
        for keyword in personality_keywords
    )

# -----------------------------------
# Technical Query Detection
# -----------------------------------

def is_technical_query(query):

    query = query.lower()

    technical_keywords = [
        "java",
        ".net",
        "python",
        "developer",
        "engineer",
        "backend",
        "frontend",
        "software",
        "programming"
    ]

    return any(
        keyword in query
        for keyword in technical_keywords
    )

# -----------------------------------
# Build Recommendation Prompt
# -----------------------------------

def build_prompt(user_query, retrieved_items):

    context = ""

    for idx, item in enumerate(retrieved_items, start=1):

        context += f"""
Assessment {idx}

Name: {item['name']}
Description: {item['description']}
Test Type: {item['test_type']}
URL: {item['url']}

"""

    prompt = f"""
User Hiring Requirement:
{user_query}

Retrieved SHL Assessments:
{context}

Task:
1. Recommend the most suitable assessments.
2. ALWAYS refer to assessments by their actual names.
3. Explain briefly why they fit.
4. Use only provided assessments.
5. Do not invent assessments or URLs.
6. Keep response concise and professional.
"""

    return prompt


# -----------------------------------
# Recommendation Pipeline
# -----------------------------------

def generate_recommendations(user_query):

    retrieved_items = retrieve_assessments(
        user_query,
        top_k=7
    )

    # -----------------------------------
    # Technical Role Prioritization
    # -----------------------------------

    if is_technical_query(user_query):

        technical_items = [
            item
            for item in retrieved_items
            if item["test_type"] == "K"
        ]

        non_technical_items = [
            item
            for item in retrieved_items
            if item["test_type"] != "K"
        ]

        retrieved_items = (
            technical_items[:4]
            + non_technical_items[:3]
        )


    # -----------------------------------
    # Personality Augmentation
    # -----------------------------------

    if requires_personality(user_query):

        personality_items = [
            item
            for item in retrieved_items
            if item["test_type"] == "P"
        ]

        technical_items = [
            item
            for item in retrieved_items
            if item["test_type"] == "K"
        ]

        other_items = [
            item
            for item in retrieved_items
            if item["test_type"] not in ["P", "K"]
        ]

        retrieved_items = (
            technical_items[:4]
            + personality_items[:2]
            + other_items[:1]
        )

    prompt = build_prompt(
        user_query,
        retrieved_items
    )

    response = clean_response(
        generate_response(prompt)
    )

    structured_recommendations = []

    for item in retrieved_items:

        structured_recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return {
        "reply": response,
        "recommendations": structured_recommendations,
        "end_of_conversation": False
    }


# -----------------------------------
# Local Testing
# -----------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("SHL Recommendation Engine")
    print("===================================\n")

    query = input("Enter hiring query: ")

    result = generate_recommendations(query)

    print("\nGenerated Recommendation:\n")

    print(result["response"])