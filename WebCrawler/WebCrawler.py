import requests
import lxml
import datetime
import sys
import re
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

#Function to parse for "name":"[content]" format. Specialize to find data in metascript
p = re.compile(r'"name":"([^"]*)"')

"""

For future use:
p can be combined with search parameters to find intended data. For example:
"isPartOf".+"name":"([^"]*)"
would find the publisher for the NYT because this is how they dictate publisher information. 
To change this parameter, one could do the following:

param = ""
p = re.compile(r'"' + param + r'".+name:"([^"]*)"')

Now param can be changed to search for the intended value. Make a list of param searches
and try to return any values that are found using them. This can be used for all 4 major 
categories of data for MLA citations. Fuck BeautifulSoup4.

"""


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
            {'rel': 'author'},
            {'class': 'byline__name'}
            ]

        author_elements = []
        for s in searches:
            author_elements += self._soup.find_all(attrs=s)

        print(author_elements)
        for el in author_elements:
           author = self.returnData(el)
           if (len(author.split()) > 1):
               authors.add(author)

        authors_list = list(authors)
        return authors_list[0]

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
            title = self.returnData(el)
            

        return title

    def findPublisher(self):

        return None
        #searches = [
        #    [{'id':'copyright'}, 'p'],
            
        #]

        #publisher_elements = []
        #for s in searches:
        #    publisher_elements += self._soup.find_all(attrs=s)

        #for el in publisher_elements:
        #    if len(el) > 0:
        #        return el.text

        #return None

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

    def returnData(self, el):
        try:
            return el['content']
        except KeyError:
            return el.text

        
    
    
    
#TESTING:
crawl = dataCrawler(BeautifulSoup(resp.text, "lxml"))

print("Printing full raw data for this URL:\n")

#print(crawl._soup.find_all(attrs={'property':'article:author'})[0].get_text())

print(crawl.findAuthor())
print(crawl.findTitle())
print(crawl.findPublisher())
print(crawl.findDate())
print(URL)
print("\nData has been printed.")