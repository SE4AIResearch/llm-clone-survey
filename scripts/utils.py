import requests


def doi_to_bibtex(doi):
    url = f"https://doi.org/{doi}"
    headers = {
        'Accept': 'application/x-bibtex'
    }
    response = requests.get(url, headers=headers)
    bibtex = response.text
    return bibtex
