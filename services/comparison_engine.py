from services.retriever import retrieve_assessments


# -----------------------------------
# Compare Assessments
# -----------------------------------

def compare_assessments(query):

    results = retrieve_assessments(
        query,
        top_k=2
    )

    if len(results) < 2:

        return (
            "I could not identify two assessments "
            "to compare."
        )

    first = results[0]
    second = results[1]

    comparison = f"""
Comparison between {first['name']} and {second['name']}:

1. {first['name']}
- Test Type: {first['test_type']}
- Description: {first['description']}

2. {second['name']}
- Test Type: {second['test_type']}
- Description: {second['description']}
"""

    return comparison