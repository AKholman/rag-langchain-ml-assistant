# scraper.py
import requests
import json
from pathlib import Path

OUT_FILE = Path("data/wikidata_ml.json")
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

QUERY = """
SELECT ?item ?itemLabel ?itemDescription WHERE {
  ?item wdt:P279* wd:Q2539.   # Q2539 = machine learning
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 5000
"""

def fetch_ml_entities():
    headers = {"Accept": "application/sparql-results+json"}
    r = requests.get(SPARQL_ENDPOINT, params={"query": QUERY}, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()

    docs = []
    for row in data["results"]["bindings"]:
        item = row["item"]["value"]
        label = row.get("itemLabel", {}).get("value", "")
        desc = row.get("itemDescription", {}).get("value", "")
        docs.append({
            "id": item.split("/")[-1],
            "title": label,
            "description": desc,
            "url": item
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

    print(f"Saved {len(docs)} ML items to {OUT_FILE}")

if __name__ == "__main__":
    fetch_ml_entities()
