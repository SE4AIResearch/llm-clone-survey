import csv
import pathlib
import time
import xml.etree.ElementTree as ET
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils import doi_to_bibtex

OUTPUT_FILE = pathlib.Path(__file__).parent.parent / "results" / "arxiv.csv"

NAMESPACE = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


def get_text(element, tag):
    found_element = element.find(tag)
    return found_element.text.strip() if found_element is not None else None


def get_arxiv_doi(paper_id):
    paper_id = paper_id.split("v")[0]
    return f"10.48550/arXiv.{paper_id}"


def parse_arxiv_response(response_content):
    papers = []
    xml_data = response_content.decode("utf-8")
    root = ET.fromstring(xml_data)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    for entry in entries:
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
        id_url = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()
        published = entry.find("{http://www.w3.org/2005/Atom}published").text.strip()
        paper_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else None
        pdf_url = id_url.replace("/abs/", "/pdf/") + ".pdf" if paper_id else None
        doi = get_text(entry, "{http://arxiv.org/schemas/atom}doi") or get_arxiv_doi(
            paper_id
        )

        papers.append(
            {
                "title": title,
                "summary": summary,
                "doi": doi,
                "pdf_url": pdf_url,
                "published": published,
                "bibtex": doi_to_bibtex(doi) if doi else "",
            }
        )

    return papers


def search_arxiv(query, max_results=50):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request failed: {e}")
        return []

    return parse_arxiv_response(response.content)


def save_papers(papers, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["doi", "url", "title", "abstract", "published", "bibtex"])
        for paper in papers:
            writer.writerow(
                [
                    paper["doi"],
                    paper["pdf_url"],
                    paper["title"],
                    paper["summary"],
                    paper["published"],
                    paper["bibtex"],
                ]
            )


if __name__ == "__main__":
    timestamp = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")

    # Break the large search into smaller valid arXiv API queries
    base_contexts = [
        "software engineering",
        "programming",
        "software development",
        "computer science",
        "computer engineering",
    ]
    clone_keywords = ["code clone", "duplicate", "clone", "redundant", "repetitive"]
    llm_keywords = [
        "LLM",
        '"large language model"',
        '"language model"',
        "GenAI",
        '"Gen AI"',
        '"Generative AI"',
        "GenerativeAI",
    ]

    queries = []
    for context in base_contexts:
        for clone_term in clone_keywords:
            for llm_term in llm_keywords:
                query = f'all:"{context}" AND all:"{clone_term}" AND all:{llm_term} AND all:code'
                queries.append(query)

    all_papers = []
    for q in queries:
        print(f"Running query: {q}")
        papers = search_arxiv(q)
        print(f"  → Found {len(papers)} papers")
        all_papers.extend(papers)

    print(f"\n✅ Total combined papers: {len(all_papers)}")

    # Deduplicate based on DOI
    seen_dois = set()
    unique_papers = []
    for p in all_papers:
        if p["doi"] not in seen_dois:
            unique_papers.append(p)
            seen_dois.add(p["doi"])

    print(f"✅ Final unique papers after deduplication: {len(unique_papers)}")
    save_papers(unique_papers, str(OUTPUT_FILE).replace(".csv", f"_{timestamp}.csv"))
