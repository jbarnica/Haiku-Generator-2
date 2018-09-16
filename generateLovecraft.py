import requests
from bs4 import BeautifulSoup
import time

WEBSITE = "http://hplovecraft.com/writings/texts/"
LOVECRAFT_DOC = "hpLovecraft.txt"

def get_links():
    r = requests.get(WEBSITE)
    soup = BeautifulSoup(r.content, 'html.parser')
    return [x.get('href') for x in soup.find_all('a') if x.get('href') is not None and 'fiction' in x.get('href') and "#fiction" not in x.get('href')]

def parse_links(links):
    pages = []
    for link in links:
        time.sleep(0.1)
        print(link)
        r = requests.get(WEBSITE+link)
        soup = BeautifulSoup(r.content, 'html.parser')
        hp_texts = soup.find_all("div", recursive=True)
        hp_text = hp_texts[2].text
        hp_text = hp_text.strip().replace("\r\n", " ")
        pages.append(hp_text)

    return pages

def process_pages(pages):
    with open(LOVECRAFT_DOC, "w+") as f:
        for page in pages:
            f.write("{}\n\n".format(page.encode('utf8')))

def generate_document():
    process_pages(parse_links(get_links()))

def return_documents():
    try:
        with open(LOVECRAFT_DOC, 'r') as f:
            text = f.read().replace('\n', '')
    except IOError:
        generate_document()
        with open(LOVECRAFT_DOC, 'r') as f:
            text = f.read().replace('\n', '')
    
    return text

if __name__ == "__main__":
    return_documents()

