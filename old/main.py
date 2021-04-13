import requests # à installer via un pip install requests dans les CMD
from bs4 import BeautifulSoup
from pprint import pprint
from python_scrap import livre_analyse
import csv
import shutil

def clear(titre: str) -> str:
    propre = ""
    for lettre in titre:
        if lettre != " ":
            propre += lettre
    return propre

#default > div > div > div > aside > div.side_categories
def liste_categories() -> dict[str, str]:
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


def livre_in_categorie(categorie: str) -> list[str]:
    """ A partir de l'url d'une catégorie cette fonction retourne
     les urls de tous les livres de cette catégorie"""
    url = categorie
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    liens = soup.find_all('h3')
    livres_url = []
    for lien in liens:
        livres_url.append("http://books.toscrape.com/catalogue/" + lien.a["href"][9:])
    return livres_url


def download(livre: dict[str, any]) -> None:
    """ Télécharge l'image liées au livre dans le dossier image"""
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


def to_csv(livre: dict[str, any], categorie: str) -> None:
    """ crée un csv par catégorie de livre"""
    file_name = "csv/"+categorie + ".csv"
    print(f"Écriture dans {file_name}")
    with open(file_name, 'w', newline='') as csv_file:
        fieldnames = list(livre.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(livre)


# Attention, il faut un csv par catégorie
def main():
    ensemble_livres = []
    for cat in liste_categories().values():
        cat_name = cat.split("/")[6][:-2].capitalize()
        print(f"\n***\t{cat_name}\t***\n")
        for livre_url in livre_in_categorie(cat):
            livre = livre_analyse(livre_url)
            print(livre_url)
            print(livre)
            ensemble_livres.append(livre)
            # Étape de téléchargement des livres
            download(livre)
            to_csv(livre, cat_name)
    return ensemble_livres

main()


# Tests
# un_livre = livre_analyse("http://books.toscrape.com/catalogue/little-women-little-women-1_331/index.html")
# pprint(un_livre)
# ownload(un_livre)
# to_csv(un_livre, "romantique")