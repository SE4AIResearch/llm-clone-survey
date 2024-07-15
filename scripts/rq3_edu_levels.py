"""
Utility script to answer RQ3.
@author: Joanna C. S. Santos
"""
from collections import defaultdict

from utils import get_educational_level, get_all_relevant_papers


def get_bibid(bibtex: str) -> str:
    """
    Given the full bibtex, extract the ID.
    :param bibtex: the full bibtex (ex: @article{DBLP:journals/corr/abs-2103-03404, ...})
    :return: returns the ID (ex: DBLP:journals/corr/abs-2103-03404)
    """
    if not bibtex:
        raise ValueError("Bibtex is empty.")
    return bibtex.strip().split("{")[1].split(",")[0]


def rq3_edu_levels(papers: list) -> dict:
    # count papers per educational level and the citations (bibtex field)
    # key: educational level, value: (total, list of bibkeys)
    edu_levels_count = defaultdict(lambda: (0, []))

    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the educational levels
        educational_levels = get_educational_level(row['paper_id'])
        for level in educational_levels:
            total, bibkeys = edu_levels_count[level]
            bibkeys.append(get_bibid(row['bibtex']))
            edu_levels_count[level] = (total + 1, bibkeys)

    return edu_levels_count


if __name__ == '__main__':
    papers = get_all_relevant_papers()
    rq3_table = rq3_edu_levels(papers)

    print("Educational levels count:")
    for edu_level, (count, citations) in rq3_table.items():
        latex_citation = "\cite{" + ','.join(citations) + "}"
        percentage = (count / len(papers)) * 100
        print(f"\t{edu_level} & {count} ({percentage:.1f}\\%) & {latex_citation} \\\\")
