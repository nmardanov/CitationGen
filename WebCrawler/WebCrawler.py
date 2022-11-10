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

    #Finds citation data from the website
    def crawlData(self):
        soup = BeautifulSoup(resp.text, "lxml")
        elements = soup.select('[rel="author"]')
        print(elements[0].text)
        elements = soup.select('title')
        print(elements[0].text)
        elements = soup.select('[class="date time published updated"]')
        print(elements[0].text)

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



owl = Citation()
owl.crawlData()