import requests
import lxml
import datetime
import sys
from bs4 import BeautifulSoup

#Connect to website given by user
URL = input("URL: ")
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
resp = requests.get(URL, headers = headers)
print(resp.status_code)

if resp.status_code != 200:
    raise Exception("Website did not connect properly. Check status code: " + str(resp.status_code))
    

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
        searches = [
            {'name': 'author'},
            {'property': 'article:author'},
            {'property': 'author'},
            {'rel': 'author'},
            {'class': 'byline__name'}
            ]

        author_elements = []
        for s in searches:
            author_elements += self._soup.find_all(attrs=s)

        for el in author_elements:
           if len(el) > 0:
               return el.text

        return None

    def findTitle(self):
        searches = [
            {'class':'title'},
            {'property':'og:title'},
            'title'
        ]

        title_elements = []
        for s in searches:
            title_elements += self._soup.find_all(attrs=s)

        for el in title_elements:
            if len(el) > 0:
                try:
                    return el['content']
                except KeyError:
                    return el.text

        return None

    def findPublisher(self):
        searches = [
            #[{'id':'copyright'}, 'p'],
            
        ]

        publisher_elements = []
        for s in searches:
            publisher_elements += self._soup.find_all(attrs=s)

        for el in publisher_elements:
            if len(el) > 0:
                return el.text

        return None

    def findDate(self):
        searches = [
            
        ]

        date_elements = []
        for s in searches:
            date_elements += self._soup.find_all(attrs=s)

        for el in date_elements:
            if len(el) > 0:
                return el.text

        return None
    
    
    
#TESTING:
crawl = dataCrawler(BeautifulSoup(resp.text, "lxml"))

print("Printing full raw data for this URL:\n")
print(crawl.findAuthor())
print(crawl.findTitle())
print(crawl.findPublisher())
print(crawl.findDate())
print(URL)
print("\nData has been printed.")