"""
Utility script to generate a .bib file for all studied papers.
It standardizes the bibtex ID based on the first author, year, and first word in the title.
@author: Joanna C. S. Santos
"""

from utils import get_all_relevant_papers, generate_bibtex_id, get_bibid, shorten_bibtex
# import sqlite3
# def update(conn, paper_id, bibtex):
#     cursor = conn.cursor()
#     #     run parameterized query
#     a = cursor.execute("UPDATE llm_education_survey_paper SET bibtex = ? WHERE id = ?", (bibtex, paper_id))
#     print(a)
#     conn.commit()
#
# if __name__ == '__main__':
#     # Connect to the SQLite database
#     conn = sqlite3.connect('../../coding_website/db_llm_education_survey.sqlite3')
#
#
#     output_file = "../results/slr_papers.sql"
#     papers = get_all_relevant_papers()
#     abbreviate_authors = False
#     print(f"Generating a .bib file for {len(papers)} papers.")
#     with open(output_file, "w") as f:
#         for _, row in papers.iterrows():
#             bibtex = row['bibtex'].strip()
#
#             if not bibtex:
#                 raise ValueError(f"Paper {row['paper_id']} has no bibtex.")
#
#             old_bib_id = get_bibid(bibtex)
#             new_bib_id = generate_bibtex_id(bibtex)
#             if abbreviate_authors:
#                 bibtex = shorten_bibtex(bibtex)
#             bibtex = bibtex.replace(old_bib_id, new_bib_id)
#             f.write(f"UPDATE llm_education_survey_paper SET bibtex = '{bibtex}' WHERE paper_id = '{row['paper_id']}';")
#             f.write("\n")
#             print(f"Paper {new_bib_id} added to {output_file}")
#             update(conn, row['paper_id'], bibtex)


if __name__ == '__main__':
    output_file = "../results/slr_papers.bib"
    papers = get_all_relevant_papers()
    abbreviate_authors = True
    print(f"Generating a .bib file for {len(papers)} papers.")
    with open(output_file, "w") as f:
        for _, row in papers.iterrows():
            bibtex = row['bibtex'].strip()

            if not bibtex:
                raise ValueError(f"Paper {row['paper_id']} has no bibtex.")

            old_bib_id = get_bibid(bibtex)
            new_bib_id = generate_bibtex_id(bibtex)
            if abbreviate_authors:
                bibtex = shorten_bibtex(bibtex)

            f.write(bibtex.replace(old_bib_id, new_bib_id))
            f.write("\n\n")
            print(f"Paper {new_bib_id} added to {output_file}")
            print(shorten_bibtex(bibtex))
