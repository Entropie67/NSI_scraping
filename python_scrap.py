
import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

def livre_analyse(url):
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    titre = soup.title.text
    table = soup.table.find_all('td')
    image_url = "http://books.toscrape.com" + soup.img['src'][5:]
    for info in table:
        print(info.text)
    print(table)
    description = soup.find_all('p')[3].text
    print(description)
    return titre, image_url, description

print(livre_analyse(url))