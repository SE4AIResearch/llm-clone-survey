"""
Utility script to answer the RQs.
@author: Joanna C. S. Santos
"""
from collections import defaultdict

from scripts.utils import generate_bibtex_id, get_llms
from utils import get_educational_level, get_all_relevant_papers

TABLE_HEADER_WITH_CITATIONS = """\\begin{table}[ht]
    \\centering
    \\caption{<<CAPTION>>}
    \\begin{tabular}{l c p{4cm}}
        \\toprule
        \\textbf{<<NAME>>} & \\textbf{\\# Papers} & \\textbf{Papers} \\\\
        \\midrule\n"""

# TABLE_HEADER_NO_CITATIONS = """\\begin{table}[ht]
#     \\centering
#     \\caption{<<CAPTION>>}
#     \\begin{tabular}{l c p{4cm}}
#         \\toprule
#         \\textbf{<<NAME>>} & \\textbf{\\# Papers} & \\textbf{\% Papers} \\\\
#         \\midrule\n"""

TABLE_HEADER_NO_CITATIONS = """\\begin{table}[ht]
    \\centering
    \\caption{<<CAPTION>>}
    \\begin{tabular}{l c p{4cm}}
        \\toprule
        \\textbf{<<NAME>>} & \\textbf{\\# Papers} \\\\
        \\midrule\n"""

TABLE_FOOTER = """\t\\bottomrule
    \\end{tabular}
    \\label{tab:<<TAB_ID>>}
\\end{table}"""


def rq1_edu_levels(papers: list) -> dict:
    """
    Count papers per educational level and the citations (bibtex field)
    :param papers: list of papers selected to be studied
    :return: key: educational level, value: (total, list of bibkeys)
    """
    edu_levels_count = defaultdict(lambda: (0, []))

    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the educational levels
        educational_levels = get_educational_level(row['paper_id'])
        for level in educational_levels:
            total, bibkeys = edu_levels_count[level]
            bibkeys.append(generate_bibtex_id(row['bibtex']))
            edu_levels_count[level] = (total + 1, bibkeys)

    return edu_levels_count


def rq2_llms(papers: list) -> dict:
    # count papers per LLM and the citations (bibtex field)
    # key: LLM, value: (total, list of bibkeys)
    llms_count = defaultdict(lambda: (0, []))

    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the educational levels
        used_llms = get_llms(row['paper_id'])
        for model in used_llms:
            total, bibkeys = llms_count[model]
            bibkeys.append(generate_bibtex_id(row['bibtex']))
            llms_count[model] = (total + 1, bibkeys)

    return llms_count


# if __name__ == '__main__':
#     papers = get_all_relevant_papers()
#     rq3_table = rq3_edu_levels(papers)
#     output_file = "../results/tables/rq3_edu_levels.tex"
#     table_header = """\\begin{table}[ht]
#     \\centering
#     \\caption{Distribution of Educational Levels where LLMs are used in CS courses.}
#     \\begin{tabular}{l c p{4cm}}
#         \\toprule
#         \\textbf{Level} & \\textbf{\\# Papers} & \\textbf{Papers} \\\\
#         \\midrule\n"""
#     table_footer = """\t\\bottomrule
#     \\end{tabular}
#     \\label{tab:rq3}
# \\end{table}"""
#     print("Educational levels count:")
#
#     with(open(output_file, "w")) as f:
#         f.write(table_header)
#         for edu_level, (count, citations) in rq3_table.items():
#             latex_citation = "\cite{" + ','.join(citations) + "}"
#             percentage = (count / len(papers)) * 100
#             f.write(f"\t\t{edu_level} & {count} ({percentage:.1f}\\%) & {latex_citation} \\\\\n")
#         f.write(table_footer)
#
#     print(f"Table saved to {output_file}")


def save_table(rq_table: dict, output_file: str, caption: str, name: str, table_id: str, with_citations: bool = True):
    table_header = TABLE_HEADER_WITH_CITATIONS if with_citations else TABLE_HEADER_NO_CITATIONS
    table_footer = TABLE_FOOTER.replace("<<TAB_ID>>", table_id)
    table_header = table_header.replace("<<CAPTION>>", caption).replace("<<NAME>>", name)

    with(open(output_file, "w")) as f:
        f.write(table_header)
        for edu_level, (count, citations) in rq_table.items():
            percentage = (count / len(papers)) * 100
            latex_citation = "\cite{" + ','.join(citations) + "}"
            if with_citations:
                f.write(f"\t\t{edu_level} & {count} ({percentage:.1f}\\\\%) & {latex_citation} \\\\\n")
            else:
                f.write(f"\t\t% {percentage:.1f}%: {latex_citation} \\\\\n")
                f.write(f"\t\t{edu_level} & {count} \\\\\n")
        f.write(table_footer)
    total_percentage = sum([count for count, _ in rq_table.values()])
    total_percentage = (total_percentage / len(papers)) * 100
    print(f"Table {table_id} saved to {output_file}")
    print(f"Total percentage: {total_percentage:.1f}%")


if __name__ == '__main__':
    papers = get_all_relevant_papers()
    rq1_table = dict(sorted(rq1_edu_levels(papers).items(), key=lambda x: x[1][0], reverse=True))
    rq1_output_file = "../results/tables/rq1_edu_levels.tex"
    rq1_caption = "Distribution of Educational Levels where LLMs are used in CS courses."
    rq1_name = "Educational Level"
    rq1_table_id = "edu_level"

    save_table(rq1_table, rq1_output_file, rq1_caption, rq1_name, rq1_table_id, False)