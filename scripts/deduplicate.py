import sqlite3

from Levenshtein import distance

THRESHOLD = 5
if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('../../coding_website/db_llm_education_survey.sqlite3')

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a SQL query
    cursor.execute('SELECT id, title, source FROM llm_education_survey_paper')

    # Fetch all results from the executed query
    rows = cursor.fetchall()

    # Compose paper list
    papers = [r for r in rows]

    with (open("../results/possible_duplicates.tsv", "w") as f):
        f.write(f"paper1_id\tpaper2_id\tsource1\tsource2\tcombined_sources\tpaper1\tpaper2\tedit_distance\n")
        for paper1_id, paper1, source1 in papers:
            for paper2_id, paper2,source2 in papers:
                if paper1_id != paper2_id and \
                    paper1_id < paper2_id and \
                        len(paper1) > THRESHOLD and \
                        len(paper2) > THRESHOLD and \
                        source1 != source2:
                    edit_distance = distance(paper1, paper2)
                    if edit_distance <= THRESHOLD:
                        clean_paper1 = paper1.replace('\t', ' ').replace('\n', ' ')
                        clean_paper2 = paper2.replace('\t', ' ').replace('\n', ' ')
                        combined_sources = f"{source1}, {source2}"
                        f.write(f"{paper1_id}\t{paper2_id}\t{source1}\t{source2}\t{combined_sources}\t{clean_paper1}\t{clean_paper2}\t{edit_distance}\n")

    # Close the connection
    conn.close()
