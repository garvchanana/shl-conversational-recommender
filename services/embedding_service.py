import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# -----------------------------
# File Paths
# -----------------------------

CATALOG_FILE = "catalog/shl_catalog_cleaned.json"

FAISS_INDEX_FILE = "embeddings/faiss_index.bin"

METADATA_FILE = "embeddings/metadata.pkl"


# -----------------------------
# Embedding Model
# -----------------------------

MODEL_NAME = "all-MiniLM-L6-v2"


# -----------------------------
# Load Catalog
# -----------------------------

def load_catalog():

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Build Searchable Text
# -----------------------------

def build_search_text(item):

    fields = [
        item.get("name", ""),
        item.get("description", ""),
        item.get("test_type", "")
    ]

    combined_text = " ".join(fields)

    return combined_text.lower()


# -----------------------------
# Main Pipeline
# -----------------------------

def main():

    print("\n===================================")
    print("Loading SHL Catalog")
    print("===================================\n")

    catalog = load_catalog()

    print(f"Loaded {len(catalog)} assessments.\n")

    print("Loading embedding model...\n")

    model = SentenceTransformer(MODEL_NAME)

    print("Preparing searchable text...\n")

    texts = [build_search_text(item) for item in catalog]

    print("Generating embeddings...\n")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    print(f"\nEmbedding Dimension: {dimension}")

    print("\nBuilding FAISS index...\n")

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print("Saving FAISS index...\n")

    faiss.write_index(index, FAISS_INDEX_FILE)

    print("Saving metadata...\n")

    with open(METADATA_FILE, "wb") as f:
        pickle.dump(catalog, f)

    print("\n===================================")
    print("Embedding Pipeline Completed")
    print("===================================")
    print(f"Index File    : {FAISS_INDEX_FILE}")
    print(f"Metadata File : {METADATA_FILE}")
    print("===================================\n")


# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    main()