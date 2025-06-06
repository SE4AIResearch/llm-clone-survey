import csv
import pathlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

OUTPUT_FILE = pathlib.Path(__file__).parent.parent / "results" / "springer.csv"
#  ("software engineering" OR "programming" OR "software development" OR "computer science" OR "computer engineering") AND ("code clone" OR "duplicat" OR “clone” OR "redundant" OR "Repetitive") AND ("code") AND ("LLM" OR "large language model" OR “language model”) OR  “GenAI” OR “Gen AI”  OR “Generative AI” OR “GenerativeAI”)
URL = "https://link.springer.com/search?new-search=true&query=%28%22software+engineering%22+OR+%22programming%22+OR+%22software+development%22+OR+%22computer+science%22+OR+%22computer+engineering%22%29+AND+%28%22code+clone%22+OR+%22duplicat%22+OR+%E2%80%9Cclone%E2%80%9D+OR+%22redundant%22+OR+%22Repetitive%22%29+AND+%28%22code%22%29+AND+%28%22LLM%22+OR+%22large+language+model%22+OR+%E2%80%9Clanguage+model%E2%80%9D%29+OR++%E2%80%9CGenAI%E2%80%9D+OR+%E2%80%9CGen+AI%E2%80%9D++OR+%E2%80%9CGenerative+AI%E2%80%9D+OR+%E2%80%9CGenerativeAI%E2%80%9D%29&dateFrom=&dateTo=&facet-discipline=%22Computer+Science%22&sortBy=relevance"


def make_request(page_num):
    return requests.get(URL + page_num).content


if __name__ == "__main__":
    timestamp = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
    csv_file = str(OUTPUT_FILE).replace(".csv", f"_{timestamp}.csv")

    with open(csv_file, "w", encoding="utf-8", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(
            ["title", "published", "link", "DOI", "authors", "content_type", "abstract"]
        )

        for i in range(1, 14):
            print("Page:", i)
            content = make_request(str(i))
            soup = BeautifulSoup(content, "html.parser")

            raw_list = soup.find_all("ol", {"class": "u-list-reset"})
            if not raw_list:
                print(f"⚠️ No articles found on page {i}")
                continue

            article_elements = raw_list[0].find_all("li")

            for article_element in article_elements:
                title_element = article_element.find(
                    "a", class_="app-card-open__link", href=True
                )
                if not title_element:
                    continue

                link = title_element["href"]
                article_url = "https://link.springer.com" + link

                try:
                    article_res = requests.get(article_url)
                    time.sleep(1)
                    article_soup = BeautifulSoup(article_res.content, "html.parser")
                except requests.exceptions.RequestException:
                    print(f"⚠️ Failed to fetch article: {article_url}")
                    continue

                # Get abstract
                abstract_tag = article_soup.find("div", {"id": "Abs1-content"})
                abstract = abstract_tag.text.strip() if abstract_tag else "No abstract"

                # Get content_type from article page
                content_type_meta = article_soup.find(
                    "meta", {"name": "citation_article_type"}
                )
                content_type = (
                    content_type_meta["content"] if content_type_meta else "N/A"
                )

                authors_element = article_element.find_all(
                    "span", {"data-test": "authors"}
                )
                published_element = article_element.find_all(
                    "span", {"data-test": "published"}
                )

                authors = authors_element[0].text if authors_element else ""
                published = published_element[0].text if published_element else ""

                index = link.find("10.")
                doi = link[index:] if index != -1 else "N/A"

                row = [
                    title_element.text.strip(),
                    published,
                    link,
                    doi,
                    authors.strip(),
                    content_type.strip(),
                    abstract,
                ]
                csvwriter.writerow(row)
