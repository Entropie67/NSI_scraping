
import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
page = requests.get(url)
html = page.text
soup = BeautifulSoup(html, "lxml")


titre = soup.title.text
table = soup.table.find_all('td')
for info in table:
    print(info.text)
print(table)
