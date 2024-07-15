"""
Utility script to generate a .bib file for all studied papers.
"""


from utils import get_all_relevant_papers

if __name__ == '__main__':
    papers = get_all_relevant_papers()
    with open("../results/slr_papers.bib", "w") as f:
        for _, row in papers.iterrows():
            f.write(row['bibtex'])
            f.write("\n\n")