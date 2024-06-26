import pathlib

from bs4 import BeautifulSoup
import requests
import time
import csv
OUTPUT_FILE = pathlib.Path(__file__).parent.parent / 'results' / 'arxiv.csv'

url='https://link.springer.com/search?new-search=true&query=%28%22software+engineering%22+OR+%22programming%22+OR+%22software+development%22+OR+%22computer+science%22+OR+%22computer+engineering%22%29+AND+%28%22education%22+OR+%22teaching%22%29+AND+%28%22LLM%22+OR+%22large+language+model%22%29&dateFrom=&dateTo=&facet-discipline=%22Computer+Science%22&sortBy=relevance&page='
# url='https://link.springer.com/search?query=%28%22machine+learning%22+OR+%22deep+learning%22+OR+%22artificial+intelligence%22%29+AND+%28%22security%22+OR+%22vulnerability%22%29+AND+%28%22code%22%29&sortOrder=oldestFirst&facet-discipline=%22Computer+Science%22&date-facet-mode=between&facet-start-year=2020&previous-start-year=2020&facet-end-year=2022&previous-end-year=2023'

def make_request(page_num):
    req = requests.get(url+page_num)
    content = req.content
    return content

with open(OUTPUT_FILE, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    fields = ['Title', 'Publication Title', 'Link', 'DOI', 'Authors', 'Year', 'Content Type']
    csvwriter.writerow(fields)

    for i in range(1, 14):
        content = make_request(str(i))
        soup = BeautifulSoup(content, 'html.parser')
        raw = soup.find(id='results-list')
        article_elements = raw.find_all("li")
        for article_element in article_elements:
            content_type = article_element.find("p", class_="content-type")
            title_element = article_element.find("a", class_="title", href=True)
            link = "https://link.springer.com/" + title_element['href']
            authors = article_element.find("span", class_="authors")
            publication = article_element.find("a", class_="publication-title")
            if(article_element.find("span", class_="year")):
                year = article_element.find("span", class_="year").text.strip("()")
            else:
                year = 'None'

            index = title_element['href'].find("10.")
            doi = title_element['href'][index:]
            if(publication):
                publication = publication.text.strip()
            else:
                publication = 'None'

            row = [title_element.text.strip(), publication, link, doi, authors.text.strip(), year, content_type.text.strip()]
            csvwriter.writerow(row)

