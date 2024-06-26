import csv
import pathlib
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from scripts.utils import doi_to_bibtex

OUTPUT_FILE = pathlib.Path(__file__).parent.parent / 'results' / 'arxiv.csv'

NAMESPACE = {
    'atom': 'http://www.w3.org/2005/Atom',  # Commonly used prefix for the Atom namespace
    'arxiv': 'http://arxiv.org/schemas/atom',  # Prefix for the ArXiv-specific namespace
    'opensearch': "http://a9.com/-/spec/opensearch/1.1/"  # Prefix for the OpenSearch-specific namespace
}


def get_text(element, tag):
    found_element = element.find(tag)
    if found_element is None:
        return None
    return found_element.text.strip()


def get_arxiv_doi(paper_id):
    paper_id = paper_id.split("v")[0]  # Remove the version number
    return f'10.48550/arXiv.{paper_id}'


def search_arxiv(query, start=0, batch_size=200):
    base_url = "http://export.arxiv.org/api/query"
    papers = []

    while True:
        params = {
            "search_query": query,
            "start": start,
            "max_results": batch_size,
            # "sortBy": "relevance",
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
            published = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            paper_id = id_url.split('/abs/')[-1] if '/abs/' in id_url else None
            pdf_url = id_url.replace('/abs/', '/pdf/') + ".pdf" if paper_id else None
            doi = get_text(entry, '{http://arxiv.org/schemas/atom}doi')
            if doi is None:
                doi = get_arxiv_doi(paper_id)

            papers.append({
                'title': title,
                'summary': summary,
                'doi': doi,
                'pdf_url': pdf_url,
                'published': published,
                "bibtex": doi_to_bibtex(doi) if doi else ""
            })

        start += batch_size

    return papers


def save_papers(papers, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['doi', 'url', 'title', 'abstract', 'published', 'bibtex'])
        for paper in papers:
            writer.writerow(
                [paper['doi'], paper['pdf_url'], paper['title'], paper['summary'], paper['published'], paper['bibtex']])


if __name__ == "__main__":
    timestamp = str(datetime.now()).split('.')[0].replace(' ', '_').replace(':', '-')
    query = (
        '(all:"software engineering" OR all:programming OR all:"software development" OR all:"computer science" OR all:"computer engineering")'
        ' AND '
        # '(all:education OR all:learning)'
        # '(all:education OR all:teaching OR all:literacy)'
        '(all:education OR all:teaching)'
        ' AND '
        '(all:LLM OR all:"large language model")')
    papers = search_arxiv(query)
    print(f"Found {len(papers)} papers")
    save_papers(papers, str(OUTPUT_FILE).replace('.csv', f'_{timestamp}.csv'))
