import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}


def get_page(url):
    """
    Fetch HTML page safely.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}")
        print(e)
        return None


def extract_test_links(html):
    """
    Extract assessment URLs from catalog page.
    """
    soup = BeautifulSoup(html, "lxml")

    links = set()

    for a_tag in soup.find_all("a", href=True):

        href = a_tag["href"]

        # Keep ONLY actual product catalog assessment pages
        if "/products/product-catalog/view/" in href:

            full_url = urljoin(BASE_URL, href)

            links.add(full_url)

    return list(links)


def extract_assessment_details(url):
    """
    Extract metadata from assessment page.
    """

    html = get_page(url)

    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    try:
        # Assessment Name
        title_tag = soup.find("h1")

        name = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Description
        meta_desc = soup.find("meta", attrs={"name": "description"})

        description = (
            meta_desc["content"].strip()
            if meta_desc and meta_desc.get("content")
            else ""
        )

        # Entire page text for feature extraction
        page_text = soup.get_text(separator=" ", strip=True).lower()

        # Better Test Type Classification

        test_type = "Unknown"

        description_lower = description.lower()

        if any(word in description_lower for word in [
            "personality",
            "motivation",
            "behavioral",
            "behavior"
        ]):
            test_type = "P"

        elif any(word in description_lower for word in [
            "knowledge",
            "technical",
            "coding",
            "programming",
            "software",
            "java",
            ".net",
            "data",
            "accounting"
        ]):
            test_type = "K"

        elif any(word in description_lower for word in [
            "ability",
            "cognitive",
            "aptitude",
            "reasoning"
        ]):
            test_type = "A"

        assessment = {
            "name": name,
            "url": url,
            "description": description,
            "test_type": test_type,
            "remote_testing": "remote testing" in page_text,
            "adaptive_irt": "adaptive/irt" in page_text
        }

        print(f"[SUCCESS] Scraped: {name}")

        return assessment

    except Exception as e:
        print(f"[ERROR] Failed parsing: {url}")
        print(e)
        return None


def main():

    print("\nFetching SHL catalog...\n")

    html = get_page(CATALOG_URL)

    if not html:
        print("[ERROR] Could not fetch catalog page.")
        return

    links = extract_test_links(html)

    print(f"\nFound {len(links)} potential assessment links.\n")

    assessments = []

    for idx, link in enumerate(links, start=1):

        print(f"[{idx}/{len(links)}] Processing...")

        data = extract_assessment_details(link)

        if data:
            assessments.append(data)

    # Remove duplicates by URL
    unique_assessments = {
        item["url"]: item for item in assessments
    }

    final_data = list(unique_assessments.values())

    # Save JSON
    with open("catalog/shl_catalog.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print("\n===================================")
    print(f"Saved {len(final_data)} assessments.")
    print("Output: catalog/shl_catalog.json")
    print("===================================\n")


if __name__ == "__main__":
    main()