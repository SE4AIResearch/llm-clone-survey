import requests


def doi_to_bibtex(doi):
    url = f"https://doi.org/{doi}"
    headers = {
        'Accept': 'application/x-bibtex'
    }
    response = requests.get(url, headers=headers)
    bibtex = response.text
    return bibtex


def doi_to_abstract(doi: str) -> str:
    if not doi:
        return ""
    email = 'joannacss@nd.edu'
    url = f"https://api.crossref.org/works/{doi}"
    headers = {'User-Agent': f'Python-requests/2.25.1 (mailto:{email})'}
    # headers = {'User-Agent': f'Python-requests/2.25.1'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        data = response.json()

        # Check if abstract is available
        if 'abstract' in data['message']:
            return data['message']['abstract']#.split("<jats:p>")[1].split("</jats:p>")[0].replace("<jats:italic>","").replace("</jats:italic>", "")
        else:
            # Optionally, parse the BibTeX to extract the abstract (simple string search)
            bibtex = doi_to_bibtex(doi)
            abstract_start = bibtex.find("abstract = {")
            if abstract_start != -1:
                abstract_start += len("abstract = {")
                abstract_end = bibtex.find("}", abstract_start)
                abstract = bibtex[abstract_start:abstract_end]
                return abstract

            return "No abstract available for this DOI."
    except requests.exceptions.RequestException as e:
        return f"An error occurred when retrieving abstract: {e}"


# print(doi_to_abstract("10.1007/s10515-024-00436-x"))  # Should return the abstract of the paper
print(doi_to_abstract("10.1007/978-3-031-46002-9_23"))
