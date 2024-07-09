"""
Utility script to answer the paper's research questions.
@author: Joanna C. S. Santos
"""
from utils import get_all_relevant_papers, get_languages, get_llms, get_educational_level, get_educational_outcomes, \
    get_research_methodologies


def rq1_languages(papers: list):
    print("RQ1: What are the languages used in the papers?")
    languages = set()
    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the languages
        languages = get_languages(row['paper_id'])
        print(row['title'])
        print("\t", languages)


def rq2_llms(papers: list):
    print("RQ2: What are the LLMs used in the papers?")
    llms = set()
    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the LLMs
        llms = get_llms(row['paper_id'])
        print(row['title'])
        print("\t", llms)


def rq3_educational_levels(papers: list):
    print("RQ3: What are the educational levels in the papers?")
    educational_levels = set()
    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the educational levels
        educational_levels = get_educational_level(row['paper_id'])
        print(row['title'])
        print("\t", educational_levels)


def rq4_educational_outcomes(papers: list):
    print("RQ4: What are the educational outcomes in the papers?")
    educational_outcomes = set()
    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the educational outcomes
        educational_outcomes = get_educational_outcomes(row['paper_id'])
        print(row['title'])
        print("\t", educational_outcomes)


def rq5_methodologies(papers: list):
    print("RQ5: What are the research methodologies in the papers?")
    methodologies = set()
    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the research methodologies
        methodologies = get_research_methodologies(row['paper_id'])
        print(row['title'])
        print("\t", methodologies)


if __name__ == "__main__":
    relevant_papers = get_all_relevant_papers()

    # rq1_languages(relevant_papers)
    # rq2_llms(relevant_papers)
    # rq3_educational_levels(relevant_papers)
    # rq4_educational_outcomes(relevant_papers)
    # rq5_methodologies(relevant_papers)
