import unittest
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

#  Tester l'extraction des données à partir d'une page web
class TestExtraction(unittest.TestCase):
    def test_extractions(self):
        # Effectuer une requête HTTP sur la page web et récupèrer le contenu HTML de la réponse
        response = requests.get('https://www.carrefour.fr/r/bio-et-ecologie/bio-petit-prix')
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraire les noms et les prix des produits de la page
        produits = []
        for product in soup.find_all('div', class_='product-tile'):
            nom = product.find('a', class_='product-tile-title').text.strip()
            prix = float(product.find('span', class_='value').text.strip().replace(',', '.'))
            produits.append({'nom': nom, 'prix': prix})
        
        # Vérifier que la liste de produits n'est pas vide
        self.assertTrue(len(produits) > 0)

# Tester l'insertion de données dans une base de données SQLite
class TestInsertion(unittest.TestCase):
    def test_insertion(self):
        # Création d'une base de données SQLite en mémoire
        conn = sqlite3.connect(':memory:')
        
        # Création d'une table pour les produits
        conn.execute('CREATE TABLE produits (nom TEXT, prix REAL)')
        
        # Insertion de données dans la table
        produits = [{'nom': 'produit 1', 'prix': 1.99}, {'nom': 'produit 2', 'prix': 2.99}]
        for produit in produits:
            conn.execute('INSERT INTO produits (nom, prix) VALUES (?, ?)', (produit['nom'], produit['prix']))
        
        # Récupération du nombre de lignes dans la table
        cursor = conn.execute('SELECT COUNT(*) FROM produits')
        result = cursor.fetchone()[0]
        
        # Vérification que le nombre de lignes correspond au nombre de données insérées
        self.assertEqual(result, len(produits))

# Tester l'affichage de données dans un dashboard
class TestDashboard(unittest.TestCase):
    def test_dashboard(self):
        # Création d'une base de données SQLite en mémoire
        conn = sqlite3.connect(':memory:')
        
        # Création d'une table pour les produits
        conn.execute('CREATE TABLE produits (nom TEXT, prix REAL)')
        
        # Insertion de données dans la table
        produits = [{'nom': 'produit 1', 'prix': 1.99}, {'nom': 'produit 2', 'prix': 2.99}]
        for produit in produits:
            conn.execute('INSERT INTO produits (nom, prix) VALUES (?, ?)', (produit['nom'], produit['prix']))
        
        # Récupération des données de la table avec pandas
        df = pd.read_sql_query('SELECT * FROM produits', conn)
        
        # Vérification que le nombre de lignes correspond au nombre de données insérées
        self.assertTrue(len(df) == len(produits))

#  Appeller la fonction main() pour exécuter les tests
if __name__ == '__main__':
    # Exécution des tests avec unittest
    unittest.main()
