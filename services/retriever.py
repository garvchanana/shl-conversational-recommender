import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# -----------------------------------
# Technical Keywords
# -----------------------------------

TECH_KEYWORDS = {
    "java",
    ".net",
    "python",
    "developer",
    "software",
    "backend",
    "frontend",
    "coding",
    "programming",
    "engineer"
}

# -----------------------------------
# Keyword Boosting
# -----------------------------------

def keyword_boost_score(query, item):

    query = query.lower()

    searchable_text = " ".join([
        item.get("name", ""),
        item.get("description", "")
    ]).lower()

    score = 0

    query_words = query.split()

    for word in query_words:

        if word in searchable_text:
            score += 1

    return score

# -----------------------------------
# Technical Relevance
# -----------------------------------

def technical_relevance_score(query, item):

    query_words = set(
        query.lower().split()
    )

    searchable_text = " ".join([
        item.get("name", ""),
        item.get("description", "")
    ]).lower()

    score = 0

    for keyword in TECH_KEYWORDS:

        if (
            keyword in query_words
            and keyword in searchable_text
        ):
            score += 2

    return score

# -----------------------------------
# Domain Filtering
# -----------------------------------

def is_irrelevant_for_technical_role(query, item):

    query = query.lower()

    technical_keywords = [
        "java",
        ".net",
        "developer",
        "engineer",
        "software",
        "backend",
        "frontend",
        "programming"
    ]

    non_technical_indicators = [
        "reservation",
        "bookkeeping",
        "accounting",
        "bank",
        "clerk"
    ]

    # Only apply filtering for technical queries
    if not any(
        word in query
        for word in technical_keywords
    ):
        return False

    searchable_text = " ".join([
        item.get("name", ""),
        item.get("description", "")
    ]).lower()

    return any(
        word in searchable_text
        for word in non_technical_indicators
    )

# -----------------------------------
# File Paths
# -----------------------------------

FAISS_INDEX_FILE = "embeddings/faiss_index.bin"

METADATA_FILE = "embeddings/metadata.pkl"


# -----------------------------------
# Embedding Model
# -----------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"


# -----------------------------------
# Load Resources
# -----------------------------------

print("\nLoading embedding model...\n")

model = SentenceTransformer(MODEL_NAME)

print("Loading FAISS index...\n")

index = faiss.read_index(FAISS_INDEX_FILE)

print("Loading metadata...\n")

with open(METADATA_FILE, "rb") as f:
    metadata = pickle.load(f)

print(f"Loaded {len(metadata)} assessments.\n")


# -----------------------------------
# Semantic Retrieval
# -----------------------------------

def retrieve_assessments(query, top_k=5):

    """
    Hybrid semantic + keyword retrieval.
    """

    # -----------------------------------
    # Semantic Search
    # -----------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype("float32")

    # Retrieve more candidates initially
    distances, indices = index.search(
        query_embedding,
        10
    )

    candidates = []

    for rank, idx in enumerate(indices[0]):

        if idx < len(metadata):

            item = metadata[idx]

            # Remove obviously irrelevant items
            if is_irrelevant_for_technical_role(
                query,
                item
            ):
                continue
            
            # Lower FAISS distance = better similarity
            semantic_score = 1 / (
                distances[0][rank] + 1
            )

            keyword_score = keyword_boost_score(
                query,
                item
            )

            technical_score = technical_relevance_score(
                query,
                item
            )
            # Hybrid score
            final_score = (
                semantic_score * 0.5
                + keyword_score * 0.2
                + technical_score * 0.3
            )

            candidates.append({
                "item": item,
                "score": final_score
            })

    # -----------------------------------
    # Re-rank by keyword boost
    # -----------------------------------

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------------
    # Deduplicate
    # -----------------------------------

    seen_urls = set()

    final_results = []

    for candidate in candidates:

        item = candidate["item"]

        if item["url"] in seen_urls:
            continue

        seen_urls.add(item["url"])

        final_results.append(item)

        if len(final_results) >= top_k:
            break

    return final_results

# -----------------------------------
# Local Testing
# -----------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("SHL Semantic Retrieval Test")
    print("===================================\n")

    query = input("Enter search query: ")

    results = retrieve_assessments(query)

    print("\nTop Matching Assessments:\n")

    for i, item in enumerate(results, start=1):

        print(f"{i}. {item['name']}")
        print(f"   Type : {item['test_type']}")
        print(f"   URL  : {item['url']}")
        print()