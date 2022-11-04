import requests
import lxml
from bs4 import BeautifulSoup

URL = input("URL: ")
resp = requests.get(URL)
print(resp.status_code)

if resp.status_code != 200:
    raise Exception("Website did not connect properly. Check status code: " + resp.status_code)
    



class Citation:
    def __init__(self, author, title, container, publisher, publish, URL):
        self.author = author
        self.title = title
        self.container = container
        self.publisher = publisher
        self.publish = publish
        self.URL = URL
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
        result.append(f"{self.URL}.")

        return ''.join(result)



#owl = Citation(input("author: "), input("title: "), input("container: "), input("publisher: "), input("publish date: "), input("URL: "))
#print(owl)