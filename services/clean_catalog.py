import json


INPUT_FILE = "catalog/shl_catalog.json"
OUTPUT_FILE = "catalog/shl_catalog_cleaned.json"


def is_valid_assessment(item):

    name = item.get("name", "").strip()

    description = item.get("description", "").strip()

    url = item.get("url", "").strip()

    # Basic validations
    if not name:
        return False

    if not description:
        return False

    if not url.startswith("https://"):
        return False

    # Remove very weak descriptions
    if len(description) < 30:
        return False

    return True


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    seen_urls = set()

    for item in data:

        if not is_valid_assessment(item):
            continue

        url = item["url"]

        # Remove duplicates
        if url in seen_urls:
            continue

        seen_urls.add(url)

        cleaned.append(item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print("\n===================================")
    print(f"Original Assessments : {len(data)}")
    print(f"Cleaned Assessments  : {len(cleaned)}")
    print(f"Saved File           : {OUTPUT_FILE}")
    print("===================================\n")


if __name__ == "__main__":
    main()