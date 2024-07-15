import sqlite3
from pathlib import Path

import pandas as pd
import requests

DATABASE_LOCATION = Path("../data/db_llm_education_survey.sqlite3")


def get_metadata(paper_id: int, metadata_name: str) -> dict:
    many_to_many_table_name = f"llm_education_survey_analysis_{metadata_name}s"
    if  "methodology" in metadata_name:
        many_to_many_table_name = f"llm_education_survey_analysis_research_methodologies"
    table_name = f"llm_education_survey_{metadata_name.replace('_', '')}"
    column_id_name = f"{metadata_name.replace('_', '')}_id"
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_LOCATION)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a SQL query
    cursor.execute(f'SELECT name FROM {table_name} '
                   f'JOIN {many_to_many_table_name} '
                   f'ON {table_name}.id = {many_to_many_table_name}.{column_id_name} '
                   f'JOIN llm_education_survey_analysis '
                   f'ON {many_to_many_table_name}.analysis_id = llm_education_survey_analysis.id '
                   f'WHERE paper_id = ?', (paper_id,))

    # fetch all the results
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def get_languages(paper_id: int) -> []:
    return get_metadata(paper_id, "language")



def get_llms(paper_id: int) -> []:
    return get_metadata(paper_id, "llm")

def get_educational_level(paper_id: int) -> []:
    return get_metadata(paper_id, "educational_level")

def get_research_methodologies(paper_id: int) -> []:
    return get_metadata(paper_id, "research_methodology")

def get_disciplines(paper_id: int) -> []:
    return get_metadata(paper_id, "discipline")

def get_educational_outcomes(paper_id: int) -> []:
    return get_metadata(paper_id, "educational_outcome")


def get_all_relevant_papers() -> pd.DataFrame:
    # Connect to the SQLite database
    conn = sqlite3.connect('../../coding_website/db_llm_education_survey.sqlite3')

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a SQL query
    cursor.execute('SELECT paper_id, title, abstract, source, bibtex FROM llm_education_survey_paper JOIN '
                   'llm_education_survey_analysis ON llm_education_survey_paper.id = llm_education_survey_analysis.paper_id '
                   'WHERE is_relevant = 1 AND user_id = 15')

    # fetch all the results in a data frame
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=['paper_id', 'title', 'abstract', 'source', 'bibtex'])


def doi_to_bibtex(doi):
    if not doi:
        return ""
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
            return data['message'][
                'abstract']  # .split("<jats:p>")[1].split("</jats:p>")[0].replace("<jats:italic>","").replace("</jats:italic>", "")
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
# print(doi_to_abstract("10.1007/978-3-031-46002-9_23"))
