from cite import *
import sys

try:
    URL = sys.argv[1]
except:
    URL = input("Enter a URL: ")

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    if "." not in URL:
        return "That isn't a URL!"

    resp = requests.get(URL, headers = headers)
    
    #Check for established connection. Return error if website did not connect.
    if resp.status_code != 200:
        return "Website did not connect properly. Check HTTP status code: " + str(resp.status_code)
    cite = Citation(URL)
    return cite.result

if __name__ == "__main__":
    print(main())