import csv
import pathlib
import xml.etree.ElementTree as ET

import requests

OUTPUT_FILE = pathlib.Path(__file__).parent.parent / 'results' / 'arxiv.csv'

NAMESPACE = {
    'atom': 'http://www.w3.org/2005/Atom',  # Commonly used prefix for the Atom namespace
    'arxiv': 'http://arxiv.org/schemas/atom'  # Prefix for the ArXiv-specific namespace
}

def search_arxiv(query, start=0, batch_size=100):
    base_url = "http://export.arxiv.org/api/query"
    papers = []

    while True:
        params = {
            "search_query": query,
            "start": start,
            "max_results": batch_size,
            "sortBy": "relevance",
            # "sortBy": "submittedDate",
            # "sortOrder": "descending",
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error if the request failed
        xml_data = response.text

        # Parse the current batch of papers
        root = ET.fromstring(xml_data)
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        if not entries:
            break  # If no more entries, exit the loop

        for entry in entries:

            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            id_url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            doi =  entry.find('{http://arxiv.org/schemas/atom}doi').text.strip() if entry.find('{http://arxiv.org/schemas/atom}doi') else None
            published = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            paper_id = id_url.split('/abs/')[-1] if '/abs/' in id_url else None
            pdf_url = id_url.replace('/abs/', '/pdf/') + ".pdf" if paper_id else None
            print("DOI",doi)
            papers.append({
                'title': title,
                'summary': summary,
                'doi': doi,
                'pdf_url': pdf_url,
                'published': published,
            })

        start += batch_size

    return papers


def save_papers(papers, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['doi', 'url','title', 'abstract', 'published'])
        for paper in papers:
            writer.writerow([paper['doi'], paper['pdf_url'],paper['title'], paper['summary'], paper['published']])


def main():
    query = '(((("software engineering" OR "programming" OR "software development" OR "computer science" OR "computer engineering") AND ("education" OR "learning")) AND ("LLM" OR "large language model")))'
    papers = search_arxiv(query)
    print(f"Found {len(papers)} papers")
    save_papers(papers, OUTPUT_FILE)


if __name__ == "__main__":
    main()
