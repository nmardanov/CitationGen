import requests
import lxml
from bs4 import BeautifulSoup

#Connect to website given by user
URL = input("URL: ")
resp = requests.get(URL)
print(resp.status_code)

if resp.status_code != 200:
    raise Exception("Website did not connect properly. Check status code: " + resp.status_code)
    

class Citation:
    def __init__(self, author="", title="", container="", publisher="", publish="", link=URL):
        self.author = author
        self.title = title
        self.container = container
        self.publisher = publisher
        self.publish = publish
        self.link = link
        self.result = self.generateCitation()

    #prints the full citation
    def __str__(self):
        return self.result

    #Concatenate citation information into one string containing the whole citation
    def generateCitation(self):
        result = []

        result.append(f"{self.author.upper()}. ")
        result.append(f"{self.title}. ")
        result.append(f"{self.container}, ")
        result.append(f"{self.publisher}, ")
        result.append(f"{self.publish}, ")
        result.append(f"{self.link}.")

        return ''.join(result)


class dataCrawler:
    def __init__(self, soup):
        self._soup = soup

    def findAuthor(self):
        authors = set()
        searches = [
            {'name': 'author'},
            {'property': 'article:author'},
            {'property': 'author'},
            {'rel': 'author'}
            ]

        author_elements = []
        for s in searches:
            author_elements += self._soup.find_all(attrs=s)

        for el in author_elements:
            author = self._get_data_from_element(el)
            if (len(author.split()) > 1):
                authors.add(author)
    
    def findTitle(self):
        searches = [
            {'property': 'og:title'}
            ]

        for s in searches: 
            el = self.soup.find(attrs=s)
            if(el is not None):
                return self._get_data_from_element(el)

        return '[[[TITLE]]]'

    def get_publication_date(self):
        searches = [
                {'name': 'date'},
                {'property': 'published_time'},
                {'name': 'timestamp'},
                {'class': 'submitted-date'},
                {'class': 'posted-on'},
                {'class': 'timestamp'},
                {'class': 'date'},

                ]
        for s in searches:
            el = self._soup.find(attrs=s)
            if (el is not None):
                return self._get_data_from_element(el)

        return '[[[PUBLICATION DATE]]]'

    def _get_data_from_element(self, el):
        try:
            return el['content']
        except KeyError:
            return el.text
    


owl = Citation()
owl.crawlData()