import sqlite3
from pathlib import Path

import pandas as pd
import requests
from pybtex.database.input import bibtex as pb
from unidecode import unidecode

DATABASE_LOCATION = Path("../data/db_llm_education_survey.sqlite3")


def get_metadata(paper_id: int, metadata_name: str) -> dict:
    many_to_many_table_name = f"llm_education_survey_analysis_{metadata_name}s"
    if "methodology" in metadata_name:
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
    conn = sqlite3.connect('../data/db_llm_education_survey.sqlite3')

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
def get_bibid(bibtex: str) -> str:
    """
    Given the full bibtex, extract the ID.
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: returns the ID (ex: DBLP:journals/corr/abs-2103-03404)
    """
    if not bibtex:
        raise ValueError("Bibtex is empty.")
    bibtex_id = bibtex.strip().split("{")[1].split(",")[0]
    if not bibtex_id:
        raise ValueError("Bibtex ID is empty.")
    return bibtex_id


def parse_bibtex(bibtex: str) -> dict:
    """
    Parse the bibtex string.
    :param bibtex:
    :return:
    """
    try:
        parser = pb.Parser()
        # return the first entry
        entries = parser.parse_string(bibtex).entries
        for _, entry in entries.items():
            return entry

    except Exception as e:
        raise ValueError("Bibtex could not be parsed. \n" + bibtex)


def get_first_author(parsed_bib) -> str:
    """
    Given the full bibtex, extract the first author.
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: the first author's last name (ex: "smith")
    This removes accents from the author's last name and replace with closes ASCII character.
    """
    return unidecode("".join(parsed_bib.persons['author'][0].last_names).lower())

def get_first_title_word(parsed_bib: pb.Entry) -> str:
    """
    Given the full bibtex, extract the first word in the title.
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: the first word in the title
    """
    if not parsed_bib:
        raise ValueError("Bibtex could not be parsed.")

    for word in parsed_bib.fields['title'].lower().split():
        if word not in ['and', 'or', 'the', 'a', 'an', 'what', 'which', 'how', 'why', 'when', 'where','from','to','on', 'in']:
            # remove accents from the word and replace with closest ASCII character
            return unidecode(word).replace(":","").replace("-","")


def clean(bibtex: str) -> str:
    """
    Clean the bibtex string by removing accents and extra spaces.
    :param bibtex:
    :return:
    """
    # remove non-alphanumeric
    bibtex = "".join([x for x in bibtex if x.isalnum()])
    return unidecode(bibtex).strip()

def generate_bibtex_id(bibtex: str) -> str:
    """
    Generate a standardized bibtex ID based on the first author, year, and first word in the title.
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: the standardized bibtex ID (ex: smith2021deep)
    """
    parsed_bib = parse_bibtex(bibtex)
    return clean(get_first_author(parsed_bib) + parsed_bib.fields['year'] + get_first_title_word(parsed_bib))


def shorten_bibtex(bibtex: str)->str:
    """
    Given a full bibtex citationm, it abbreviates the authors. FOr example, JOanna C. S. Santos become J. C. S. SAntos
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: the bibtex, but with abbreviated authors.
    """
    parsed_bib = parse_bibtex(bibtex)
    authors = parsed_bib.persons['author']
    for author in authors:
        for i in range(len(author.first_names)):
            author.first_names[i] = author.first_names[i][0] + "."
            # remove "." from the last name if it exist as last character
            if author.last_names[i][-1] == ".":
                author.last_names[i] = author.last_names[i][:-1]

    return parsed_bib.to_string("bibtex")


