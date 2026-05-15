import json


INPUT_FILE = "catalog/official_shl_catalog.json"

OUTPUT_FILE = "catalog/shl_catalog_cleaned.json"


# -----------------------------------
# Infer Test Type
# -----------------------------------

def infer_test_type(keys):

    keys_lower = [
        key.lower()
        for key in keys
    ]

    if any(
        "personality" in key
        or "behavior" in key
        for key in keys_lower
    ):
        return "P"

    if any(
        "ability" in key
        or "aptitude" in key
        for key in keys_lower
    ):
        return "A"

    return "K"


# -----------------------------------
# Load Official Catalog
# -----------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    data = json.load(f)


cleaned_catalog = []


# -----------------------------------
# Normalize Catalog
# -----------------------------------

for item in data:

    keys = item.get("keys", [])

    job_levels = item.get(
        "job_levels",
        []
    )

    searchable_description = " ".join([

        item.get("description", ""),

        " ".join(keys),

        " ".join(job_levels)

    ])

    cleaned_item = {

        "name": item.get("name", "").strip(),

        "description": searchable_description.strip(),

        "url": item.get("link", "").strip(),

        "test_type": infer_test_type(keys)
    }

    # Skip incomplete items
    if not cleaned_item["name"]:
        continue

    if not cleaned_item["url"]:
        continue

    cleaned_catalog.append(cleaned_item)


# -----------------------------------
# Save Cleaned Catalog
# -----------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        cleaned_catalog,
        f,
        indent=2,
        ensure_ascii=False
    )


print("\n===================================")
print("Official Catalog Prepared")
print("===================================\n")

print(f"Saved File : {OUTPUT_FILE}")
print(f"Assessments: {len(cleaned_catalog)}")