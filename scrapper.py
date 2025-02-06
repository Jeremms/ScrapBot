from bs4 import BeautifulSoup

def launch():
    # Charger le fichier HTML
    with open("./html/main.html", "r") as file:
        content = file.read()

    # Parser le HTML
    soup = BeautifulSoup(content, "html5lib")

    # Trouver la div avec la classe "item mepr-data"
    div = soup.find("div", class_="item mepr-data")

    # Vérifier si la div existe et extraire le texte du <span>
    if div:
        span = div.find("span")
        if span:
            print(span.text)
            return span.text
        else:
            print("Aucun <span> trouvé dans la div.")
    else:
        print("Aucune div avec la classe 'item mepr-data' trouvée.")
