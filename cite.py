import requests
from datetime import datetime
import re
from bs4 import BeautifulSoup

#Connect to URL given by user
#URL = input("URL: ")
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


resp = requests.get("https://www.washingtonpost.com/politics/2023/03/06/steve-daines-senate-republicans/", headers = headers)

#Citation class. Inputs URL then uses data from dataCrawler class to generate and format a citation.
class Citation:
    def __init__(self, _URL):
        self._URL = _URL
        resp = requests.get(_URL)
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

        if self.data['author'] != None:
            result.append(f"{self.data['author']}. ")
        else:
            handle = input("No author found. Manually enter an author, or type N to continue.")
            if handle != 'N':
                result.append(f"{handle}. ")

        if self.data['title'] != None:
            result.append(f"\"{self.data['title']}.\" ")
        else:
            handle = input("No title found. Manually enter a title, or type N to continue.")
            if handle != 'N':
                result.append(f"{handle}. ")

        if self.data['publisher'] != None:
            result.append(f"{self.data['publisher']}, ")
        else:
            handle = input("No publisher found. Manually enter a publisher, or type N to continue.")
            if handle != 'N':
                result.append(f"{handle}. ")

        if self.data['date'] != None:
            result.append(f"{self.data['date']}, ")
        else:
            handle = input("No date found. Manually enter a date, or type N to continue.")
            if handle != 'N':
                result.append(f"{handle}. ")

        result.append(f"{self.data['URL']}. ")
        result.append(f"Accessed {datetime.now().strftime('%d %b, %Y')}.")

        return ''.join(result)
    
    #Return individual data items
    def getItem(self, item: str):
        try:
            return self.data[item]
        except:
            return "silly! pick a valid item."
    


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
            1/len(authors_list[0]) #Escapes try block if author length is 0, which sometimes occurs in input boxes with the 'name="author"' tag
            if len(authors_list) > 3:
                return authors_list[0].title() + ' et al'
            return ', '.join(authors_list).title()
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
        except: 
            return None

    def returnData(self, el):
        try:
            return el['content']
        except KeyError:
            return el.text



def returnData(URL, item):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    resp = requests.get(URL, headers = headers)
    print(resp.status_code)

    #Check for established connection. Return error if website did not connect.
    if resp.status_code != 200:
        raise Exception("Website did not connect properly. Check HTTP status code: " + str(resp.status_code))

    cite = Citation(URL)
    return cite.data[item] 

def updateCitation(URL, author, publisher, title, date):
    pass
    
def test():
    print("test!!!")

if __name__=="__main__":
    test()