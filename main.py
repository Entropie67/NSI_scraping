import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup
from pprint import pprint
def clear(titre):
    propre = ""
    for lettre in titre:
        if lettre != " ":
            propre += lettre
    return propre

url  = "http://books.toscrape.com/catalogue/category/books_1/index.html"
page = requests.get(url)
html = page.text
soup = BeautifulSoup(html, "lxml")

#default > div > div > div > aside > div.side_categories

liens = soup.aside.find_all('a')
categories = {}
for lien in liens[1:]:
    url_cat = "http://books.toscrape.com/catalogue/category" + lien['href'][3:]
    categories[clear(lien.text.replace("\n", ""))] = url_cat
pprint(categories)

