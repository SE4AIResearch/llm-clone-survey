from bs4 import BeautifulSoup
import requests
import time
import csv

url='https://link.springer.com/search?query=%28%22machine+learning%22+OR+%22deep+learning%22+OR+%22artificial+intelligence%22%29+AND+%28%22security%22+OR+%22vulnerability%22%29+AND+%28%22code%22%29&sortOrder=oldestFirst&facet-discipline=%22Computer+Science%22&date-facet-mode=between&facet-start-year=2020&previous-start-year=2020&facet-end-year=2022&previous-end-year=2023'
req=requests.get(url)
content=req.content

soup=BeautifulSoup(content, 'html.parser')


raw=soup.find(id='results-list')

with open("springer papers.csv", 'a') as csvfile:
        csvwriter = csv.writer(csvfile) 
        
        #fields = ['Title', 'Publication Title', 'Link', 'DOI', 'Authors', 'Year', 'Content Type']
        #csvwriter.writerow(fields) 

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

        print('done')


        for i in range(2,827):
            time.sleep(3)
            url='https://link.springer.com/search/page/' + str(i) + '?query=%28%22machine+learning%22+OR+%22deep+learning%22+OR+%22artificial+intelligence%22%29+AND+%28%22security%22+OR+%22vulnerability%22%29+AND+%28%22code%22%29&sortOrder=oldestFirst&facet-discipline=%22Computer+Science%22&date-facet-mode=between&facet-start-year=2020&previous-start-year=2020&facet-end-year=2022&previous-end-year=2023'
            req=requests.get(url)
            content=req.content

            soup=BeautifulSoup(content, 'html.parser')

            raw=soup.find(id='results-list')

            article_elements = raw.find_all("li")
            for article_element in article_elements:
                content_type = article_element.find("p", class_="content-type")
                title_element = article_element.find("a", class_="title", href=True)
                authors = article_element.find("span", class_="authors")
                publication = article_element.find("a", class_="publication-title")
                doiFinder = article_element.find("a", class_="webtrekk-track pdf-link", doi=True)
                
                if(title_element):
                    index = title_element['href'].find("10.")
                    doi = title_element['href'][index:]
                else:
                    doi = 'None'
                if(publication):
                 publication = publication.text.strip()
                else:
                    publication = 'None'

                if(authors):
                    authors = authors.text.strip()
                else:
                    authors = 'None'

                if(article_element.find("span", class_="year")):
                    year = article_element.find("span", class_="year").text.strip("()")
                else:
                    year = 'None'

                if title_element:
                    link = "https://link.springer.com/" + title_element['href']
                    title_element = title_element.text.strip()
                else:
                    title_element = 'None'
                    link = 'None'

                if(content_type):
                    content_type = content_type.text.strip()
                else:
                    content_type = "None"

                row = [title_element, publication, link, doi, authors, year, content_type]
                csvwriter.writerow(row)
            print('done')
            
            