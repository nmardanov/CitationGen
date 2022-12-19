import requests
from datetime import datetime
import re
from bs4 import BeautifulSoup

#Connect to URL given by user
URL = input("URL: ")
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
resp = requests.get(URL, headers = headers)
print(resp.status_code)

#Check for established connection. Return error if website did not connect.
if resp.status_code != 200:
    raise Exception("Website did not connect properly. Check HTTP status code: " + str(resp.status_code))


"""
Current known edge cases: 
-Multiple authors
-No ld+json script

TODO:
Frontend website w/ editing
Exceptions for when data returns None
Store citations on one page, ordered alphabetically
Maybe save citations in email? or create text document with citations?
"""

#Citation class. Inputs URL then uses data from dataCrawler class to generate and format a citation.
class Citation:
    def __init__(self, _URL=URL):
        self._URL = _URL
        self.crawl = dataCrawler(BeautifulSoup(resp.text, "lxml"))
        self.data = {
            'author' : self.crawl.findAuthor(),
            'title' : self.crawl.findTitle(),
            'publisher' : self.crawl.findPublisher(),
            'date' : self.crawl.findDate(),
            'URL' : self._URL
        }
        self.result = self.generateCitation()

    #prints the full citation
    def __str__(self):
        return self.result

    #Concatenate citation information into one string containing the whole citation
    def generateCitation(self):
        result = []

        result.append(f"{self.data['author'].title()}. ")
        result.append(f"{self.data['title']}. ")
        result.append(f"{self.data['publisher']}, ")
        result.append(f"{self.data['date']}, ")
        result.append(f"{self.data['URL']}, ")
        result.append(f"date accessed: {datetime.now().strftime('%d %b, %Y')}.")

        return ''.join(result)
    


#Web scraper class. Inputs URL then finds data from website using BS4 and regex. Data is formatted ready for citation use.
class dataCrawler:
    def __init__(self, soup):
        #Initialize soup with given URL
        self._soup = soup

        #Find the ld+json script and return its contents as a string
        self._ld = str(self._soup.find('script', {'type': 'application/ld+json'}))

    #Return author from given searches
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

        for el in author_elements:
           author = self.returnData(el)
           if (len(author.split()) > 1):
               authors.add(author)

        authors_list = list(authors)

        try:
            return authors_list[0]
        except:
            return None

    #Return title from given searches, or from <title> HTML tag
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

    #Return publisher from ld+json script on most websites. May need to be expanded for sites without and ld+json script.
    def findPublisher(self):

        searches = [
            'isPartOf',
            'publisher'
        ]

        publisher_elements = []
        for s in searches:
            #Compiles for first instance of search, then for first appearance of "name": and captures whatever follows.
            p = re.compile(s+r'.+?"name":"([^"]*)"')
            publisher_elements += p.findall(self._ld)

        try:
            return publisher_elements[0]
        except:
            return None

    #Finds date from ld+json script
    #TODO: Ignore empty list elements when returning
    def findDate(self):
        
        searches = [
            'datePublished',
            'dateModified'
        ]

        date_elements = []
        for s in searches:
            #Compiles for first isntance of search, then captures whatever follows.
            p = re.compile(s + r'":"([^"]*)T')
            date_elements += p.findall(self._ld)

        try:
            dateFormat = datetime.fromisoformat(date_elements[0])
            return dateFormat.strftime('%d %b, %Y')
        except KeyError: 
            return None

    def returnData(self, el):
        try:
            return el['content']
        except KeyError:
            return el.text

        
    
    
    
#TESTING:
cite = Citation(URL)

print("Printing full raw data for this URL:\n")

#print(crawl._soup.find_all(attrs={'property':'article:author'})[0].get_text())

print(cite.data['author'])
print(cite.data['title'])
print(cite.data['publisher'])
print(cite.data['date'])
print(cite.data['URL'])

print(cite.generateCitation())

print("\nData has been printed.")