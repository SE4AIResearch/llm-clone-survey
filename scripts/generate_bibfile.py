"""
Utility script to generate a .bib file for all studied papers.
It standardizes the bibtex ID based on the first author, year, and first word in the title.
@author: Joanna C. S. Santos
"""

from utils import get_all_relevant_papers, generate_bibtex_id, get_bibid

if __name__ == '__main__':
    output_file = "../results/slr_papers.bib"
    papers = get_all_relevant_papers()
    print(f"Generating a .bib file for {len(papers)} papers.")
    with open(output_file, "w") as f:
        for _, row in papers.iterrows():
            bibtex = row['bibtex'].strip()

            if not bibtex:
                raise ValueError(f"Paper {row['paper_id']} has no bibtex.")

            old_bib_id = get_bibid(bibtex)
            new_bib_id = generate_bibtex_id(bibtex)

            f.write(bibtex.replace(old_bib_id, new_bib_id))
            f.write("\n\n")
            print(f"Paper {new_bib_id} added to {output_file}")
