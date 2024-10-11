"""
Utility script to answer the RQs.
@author: Joanna C. S. Santos
"""
from collections import defaultdict

from utils import generate_bibtex_id, get_disciplines, get_research_methodologies, get_llms, get_paper_type
from utils import get_educational_level, get_all_relevant_papers
from utils import get_languages

TABLE_HEADER_WITH_CITATIONS = """\\begin{table}[!htbp]
    \\footnotesize
    \\centering
    \\caption{<<CAPTION>>}
    \\begin{tabular}{@{}l c p{4cm}@{}}
        \\toprule
        \\textbf{<<NAME>>} & \\textbf{\\# Papers} & \\textbf{References} \\\\
        \\midrule\n"""

TABLE_HEADER_NO_CITATIONS = """\\begin{table}[ht]
    \\footnotesize
    \\centering
    \\caption{<<CAPTION>>}
    \\begin{tabular}{@{}l c@{}}
        \\toprule
        \\textbf{<<NAME>>} & \\textbf{\\# Papers} \\\\
        \\midrule\n"""

TABLE_FOOTER = """\t\\bottomrule
    \\end{tabular}
    \\label{tab:<<TAB_ID>>}
\\end{table}"""


def rq_table(papers: list, callback) -> dict:
    """
    Count papers per metadata and the citations (bibtex field)
    :param papers: list of papers selected to be studied
    :return: key: research metadata, value: (total, list of bibkeys)
    """
    counts = defaultdict(lambda: (0, []))

    # iterate data frame rows
    for _, row in papers.iterrows():
        # get the research metadata
        metadata = callback(row['paper_id'])
        for metadata in metadata:
            total, bibkeys = counts[metadata]
            bibkeys.append(generate_bibtex_id(row['bibtex']))
            counts[metadata] = (total + 1, bibkeys)

    return counts


def save_table(rq_table: dict, output_file: str, caption: str, name: str, table_id: str, with_citations: bool = True):
    table_header = TABLE_HEADER_WITH_CITATIONS if with_citations else TABLE_HEADER_NO_CITATIONS
    table_footer = TABLE_FOOTER.replace("<<TAB_ID>>", table_id)
    table_header = table_header.replace("<<CAPTION>>", caption).replace("<<NAME>>", name)

    with(open(output_file, "w")) as f:
        f.write(table_header)
        for row_name, (count, citations) in rq_table.items():
            # if count >= 3: # ignore rows with less than 3 papers
            #     continue
            percentage = (count / len(papers)) * 100
            latex_citation = "\cite{" + ','.join(sorted(citations)) + "}"
            if with_citations:
                f.write(f"\t\t{row_name} & {count} & {latex_citation} \\\\\n")
            else:
                # f.write(f"\t\t% {row_name}~{latex_citation}\n")
                f.write(f"\t\t{row_name} & {count} \\\\\n")
        f.write(table_footer)
    total_percentage = sum([count for count, _ in rq_table.values()])
    total_percentage = (total_percentage / len(papers)) * 100
    # print(f"Table {table_id} saved to {output_file}")
    # print(f"Total percentage: {total_percentage:.1f}%")


if __name__ == '__main__':
    papers = get_all_relevant_papers()
    # Educational Levels
    rq1_table = rq_table(papers, get_educational_level)
    rq1_table = dict(sorted(rq1_table.items(), key=lambda x: x[1][0], reverse=True))
    rq1_output_file = "../results/tables/rq1_edu_levels.tex"
    rq1_caption = "Distribution of Educational Levels where LLMs are used in CS courses."
    rq1_name = "Educational Level"
    rq1_table_id = "edu_level"
    save_table(rq1_table, rq1_output_file, rq1_caption, rq1_name, rq1_table_id, False)
    save_table(rq1_table, rq1_output_file.replace(".tex", "_with_citations.tex"), rq1_caption, rq1_name, rq1_table_id, True)
    # Disciplines
    rq2_table = rq_table(papers, get_disciplines)
    rq2_table = dict(sorted(rq2_table.items(), key=lambda x: x[1][0], reverse=True))
    rq2_output_file = "../results/tables/rq2_disciplines.tex"
    rq2_caption = "CS Disciplines Explored by the Studied Papers."
    rq2_name = "CS Discipline"
    rq2_table_id = "disciplines"
    save_table(rq2_table, rq2_output_file, rq2_caption, rq2_name, rq2_table_id, False)
    save_table(rq2_table, rq2_output_file.replace(".tex", "_with_citations.tex"), rq2_caption, rq2_name, rq2_table_id,
               True)

    # Research Methodologies
    rq3_table = rq_table(papers, get_research_methodologies)
    rq3_table = dict(sorted(rq3_table.items(), key=lambda x: x[1][0], reverse=True))
    rq3_output_file = "../results/tables/rq3_research_methodologies.tex"
    rq3_caption = "Research Methodologies used by the Papers."
    rq3_name = "Research Methodology"
    rq3_table_id = "methodologies"
    save_table(rq3_table, rq3_output_file, rq3_caption, rq3_name, rq3_table_id, False)
    save_table(rq3_table, rq3_output_file.replace(".tex", "_with_citations.tex"), rq3_caption, rq3_name, rq3_table_id,
               True)

    # Programming languages
    rq4_table = rq_table(papers, get_languages)
    rq4_table = dict(sorted(rq4_table.items(), key=lambda x: x[1][0], reverse=True))
    rq4_output_file = "../results/tables/rq4_languages.tex"
    rq4_caption = "Distribution of Programming Languages used in CS courses."
    rq4_name = "Programming Language"
    rq4_table_id = "languages"
    save_table(rq4_table, rq4_output_file, rq4_caption, rq4_name, rq4_table_id, False)
    save_table(rq4_table, rq4_output_file.replace(".tex", "_with_citations.tex"), rq4_caption, rq4_name, rq4_table_id,
               True)

    # LLMs used
    rq5_table = rq_table(papers, get_llms)
    rq5_table = dict(sorted(rq5_table.items(), key=lambda x: x[1][0], reverse=True))
    rq5_output_file = "../results/tables/rq5_llms.tex"
    rq5_caption = "Distribution of LLMs used by the papers."
    rq5_name = "LLM"
    rq5_table_id = "llms"
    save_table(rq5_table, rq5_output_file, rq5_caption, rq5_name, rq5_table_id, False)
    save_table(rq5_table, rq5_output_file.replace(".tex", "_with_citations.tex"), rq5_caption, rq5_name, rq5_table_id,
               True)



    # filter papers whose type = Survey
    survey_papers = papers[papers['type'] == 'Survey']
    application_papers = papers[papers['type'] == 'Application']
    technique_papers = papers[papers['type'] == 'Representation']

    application_papers_table = dict(sorted(rq_table(application_papers, get_disciplines).items(), key=lambda x: x[1][0], reverse=True))
    print("=== APPLIED PAPERS ===")
    for key, value in application_papers_table.items():
        print(f"{key.replace('ACM: ','')}: {value[0]}")
    print("=== LLM-BASED TECHNIQUE PAPERS ===")
    technique_papers_table = dict(sorted(rq_table(technique_papers, get_disciplines).items(), key=lambda x: x[1][0], reverse=True))
    for key, value in technique_papers_table.items():
        print(f"{key.replace('ACM: ','')}: {value[0]}")



