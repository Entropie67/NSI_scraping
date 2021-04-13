import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup
from pprint import pprint


def livre_analyse(url: str) -> dict[str, any]:
    """ Permet d'analyser un livre A partir de l'url du livre permet de retourner
    le titre, l'url de l'image et la description"""
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    titre = soup.title.text
    titre = titre.replace("\n", "")
    table = soup.table.find_all('td')
    image_url = "http://books.toscrape.com" + soup.img['src'][5:]
    code = table[0].text
    prix = table[3].text
    prix = prix[2:]
    disponible = table[5].text
    description = soup.find_all('p')[3].text
    info = {"Code": code, "Titre": titre, "Image url": image_url, "Description": description, "Prix": prix, "Disponibilité": disponible}
    return info

# Pour tester la fonction
# url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
# pprint(livre_analyse(url))