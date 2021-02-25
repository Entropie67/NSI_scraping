import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup
from pprint import pprint
from python_scrap import livre_analyse
import csv
import shutil

def clear(titre):
    propre = ""
    for lettre in titre:
        if lettre != " ":
            propre += lettre
    return propre


#default > div > div > div > aside > div.side_categories
def liste_categories():
    """Retourne un dictionnaire avec les catégories"""
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    liens = soup.aside.find_all('a')
    categories = {}
    for lien in liens[1:]:
        url_cat = "http://books.toscrape.com/catalogue/category/" + lien['href'][3:]
        categories[clear(lien.text.replace("\n", ""))] = url_cat
    return categories

def livre_in_categorie(categorie):
    """extrait les livres d'une  catégorie"""
    url = categorie
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    liens = soup.find_all('h3')
    livres_url = []
    for lien in liens:
        livres_url.append("http://books.toscrape.com/catalogue/" + lien.a["href"][9:])
    return livres_url

ensemble_livres = []
print(liste_categories())
def afficher():
    for cat in liste_categories().values():
        for livre_url in livre_in_categorie(cat):
            print(livre_url)
            ensemble_livres.append(livre_analyse(livre_url))
            print(livre_analyse(livre_url))
    return ensemble_livres

print("*****************")
un_livre = livre_analyse("http://books.toscrape.com/catalogue/little-women-little-women-1_331/index.html")
pprint(un_livre)

def download(livre):
    url = livre['Image url']
    titre = livre['Titre'].split("|")
    titre = titre[0].split()
    titre = "_".join(titre)
    titre = titre + ".jpg"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open("images/"+titre, 'wb') as file:
            shutil.copyfileobj(r.raw, file)
            print(f"{titre} bien téléchargée" )
    else:
        print("image indisponible")
    print(titre)
    print(url)

#download(un_livre)

print(list(un_livre.keys()))

def to_csv(livre):
    with open("livre.csv", 'w', newline='') as csv_file:
        fieldnames = list(livre.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(livre)

to_csv(un_livre)