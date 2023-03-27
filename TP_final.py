import requests
import pymongo
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, jsonify
import streamlit as st
import pandas as pd
import altair as alt


# Récupérer le contenu de la page web
# Initialiser avec l'URL de la page que nous voulons extraire
url = "https://www.carrefour.fr/r/bio-et-ecologie/bio-petit-prix"
# Utiliser la méthode GET pour envoyer une requête à l'URL spécifiée
response = requests.get(url)
# Récupérer le contenu HTML de la page web que nous voulons extraire
content = response.content

# La bibliothèque BeautifulSoup permet de parser et de naviguer dans un document HTML (ou XML) et d'extraire les informations souhaitées
# Analyser le contenu de la page web avec Beautiful Soup
soup = BeautifulSoup(content, 'html.parser')

# Le script cherche les éléments HTML qui contiennent les données que nous souhaitons extraire
# Trouver les éléments HTML qui contiennent les données que vous souhaitez extraire
data = []
for product in soup.find_all('div', {'class': 'product-tile'}):
    name = product.find('div', {'class': 'product-tile__name'}).text.strip()
    price = product.find('div', {'class': 'product-tile__price'}).text.strip()
    data.append([name, price])
    

# Initialiser l'application Flask
app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['bdd_produits']
collection = db['produits']

# Scraper le site Web et stocker les données dans MongoDB
def scraper():
    # Récupérer le contenu de la page web
    url = "https://www.carrefour.fr/r/bio-et-ecologie/bio-petit-prix"
    response = requests.get(url)
    content = response.content

    # Analyser le contenu de la page web avec Beautiful Soup
    soup = BeautifulSoup(content, 'html.parser')

    # Récupérer les informations de chaque produit et les stocker dans une liste
    data = []
    for product in soup.find_all('div', {'class': 'product-tile'}):
        name = product.find('div', {'class': 'product-tile__name'}).text.strip()
        price = product.find('div', {'class': 'product-tile__price'}).text.strip()
        data.append({'name': name, 'price': price})

    # Établir une connexion avec la base de données MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["bdd_produits"]
    collection = database["produits"]

    # Insérer les données dans la base de données
    if data:
        collection.insert_many(data)
    else:
        print("Error: data is empty")
    
# Définir une route pour l'API qui renvoie les données sous forme de tableau JSON
@app.route('/api/produits', methods=['GET'])
def get_data():
    produits = []
    for doc in collection.find():
        doc['_id'] = str(doc['_id'])
        produits.append(doc)
    return jsonify(produits)

if __name__ == '__main__':
    scraper()
    app.run()


# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['bdd_produits']
collection = db['produits']

# Récupérer les données de la base de données MongoDB et les stocker dans un DataFrame Pandas
data = []
for doc in collection.find():
    doc['_id'] = str(doc['_id'])
    data.append(doc)
df = pd.DataFrame(data)

# Créer un graphique à l'aide de la bibliothèque Altair
chart = alt.Chart(df).mark_bar().encode(
    x='name',
    y='price',
    color='name'
).properties(
    width=800,
    height=500
)

# Afficher le tableau et le graphique dans l'application Streamlit
st.title('Tableau de produits')
st.write(df)
st.title('Graphique de produits')
st.altair_chart(chart)
