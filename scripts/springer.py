import csv
import pathlib
from datetime import datetime

import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = pathlib.Path(__file__).parent.parent / 'results' / 'springer.csv'

# ("software engineering" OR "programming" OR "software development" OR "computer science" OR "computer engineering") AND ("education" OR "teaching") AND ("LLM" OR "large language model")
URL = 'https://link.springer.com/search?new-search=true&query=%28%22software+engineering%22+OR+%22programming%22+OR+%22software+development%22+OR+%22computer+science%22+OR+%22computer+engineering%22%29+AND+%28%22education%22+OR+%22teaching%22%29+AND+%28%22LLM%22+OR+%22large+language+model%22%29&dateFrom=&dateTo=&facet-discipline=%22Computer+Science%22&sortBy=relevance&page='


def make_request(page_num):
    req = requests.get(URL + page_num)
    return req.content


if __name__ == "__main__":

    timestamp = str(datetime.now()).split('.')[0].replace(' ', '_').replace(':', '-')
    csv_file = str(OUTPUT_FILE).replace('.csv', f'_{timestamp}.csv')
    with open(csv_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        fields = ['title', 'published', 'link', 'DOI', 'authors', 'content_type']
        csvwriter.writerow(fields)

        # loop through the pages (I've seen that there are 13 pages)
        for i in range(1, 14):
            print("Page: ", i)
            content = make_request(str(i))
            soup = BeautifulSoup(content, 'html.parser')
            # find the first div whose class = u-list-reset
            raw = soup.find_all("ol", {"class": "u-list-reset"})[0]
            article_elements = raw.find_all("li")
            for article_element in article_elements:
                meta_div = article_element.find("div", {"class": "c-meta"})
                content_type = meta_div.find_all("span", {"data-test": "content-type"})[0].text

                title_element = article_element.find("a", class_="app-card-open__link", href=True)
                authors_element = article_element.find_all("span", {"data-test": "authors"})
                published_element = article_element.find_all("span", {"data-test": "published"})

                link = title_element['href']
                index = title_element['href'].find("10.")
                doi = title_element['href'][index:]

                authors = authors_element[0].text if authors_element else ""
                published = published_element[0].text if published_element else ""

                row = [title_element.text.strip(), published, link, doi, authors.strip(), content_type.strip()]
                csvwriter.writerow(row)
