import pandas as pd
import re

# Function to parse the BibTeX file
def parse_bib_file_with_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    entries = re.split(r'@(\w+){', content)[1:]
    parsed_entries = []
    bib_entries = []

    for i in range(0, len(entries), 2):
        entry_type = entries[i]
        entry_content = "{" + entries[i+1]
        fields = re.findall(r'(\w+)\s*=\s*[{"]([^{}"]+)[}"]', entry_content)
        entry_dict = {field: value for field, value in fields}
        entry_dict['type'] = entry_type
        parsed_entries.append(entry_dict)
        bib_entries.append(f"@{entry_type}{entry_content}")

    return pd.DataFrame(parsed_entries), bib_entries

if __name__ == '__main__':

    # Parse the two uploaded .bib files
    acm_df, acm_bib_entries = parse_bib_file_with_entries('../results/acm_export2024.07.02-16.14.bib')
    sciencedirect_df, sciencedirect_bib_entries = parse_bib_file_with_entries('../results/ScienceDirect_2024-06-26_17-18-04.bib')

    # Add the 'bibtex' column
    acm_df['bibtex'] = acm_bib_entries
    sciencedirect_df['bibtex'] = sciencedirect_bib_entries

    # Convert necessary columns to string type if needed
    # For demonstration, converting 'title' column to string type
    acm_df['title'] = acm_df['title'].astype(str)
    sciencedirect_df['title'] = sciencedirect_df['title'].astype(str)

    # import ace_tools as tools; tools.display_dataframe_to_user(name="ACM Export Data with BibTeX", dataframe=acm_df)
    # import ace_tools as tools; tools.display_dataframe_to_user(name="ScienceDirect Export Data with BibTeX", dataframe=sciencedirect_df)

    # Save the DataFrames as CSV files with BibTeX
    acm_csv_path = '../results/acm_export2024.07.02-16.14.csv'
    sciencedirect_csv_path = '../results/ScienceDirect_2024-06-26_17-18-04.csv'

    acm_df.to_csv(acm_csv_path, index=False)
    sciencedirect_df.to_csv(sciencedirect_csv_path, index=False)


    print("ACM Export Data with BibTeX:")
    print(acm_df.head())
    print("\nScienceDirect Export Data with BibTeX:")
    print(sciencedirect_df.head())