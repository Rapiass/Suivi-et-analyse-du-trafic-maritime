from fastapi import HTTPException
import mariadb
import sys

# Définition de la classe Database pour gérer la connexion à la base de données MariaDB
class Database:
    def __init__(self):
        try:
            # Tentative de connexion à la base de données MariaDB
            self.conn = mariadb.connect(
                user="user",  # Nom d'utilisateur pour se connecter à la base de données
                password="password",  # Mot de passe pour se connecter à la base de données
                host="db",  # Adresse de l'hôte de la base de données (db correspond à ton conteneur DB)
                port=3306,  # Port utilisé pour la connexion à la base de données MariaDB
                database="bd_projet_AIS"  # Nom de la base de données à laquelle se connecter
            )
            # Création d'un curseur pour exécuter des requêtes SQL
            self.cursor = self.conn.cursor(dictionary=True)
        except mariadb.Error as e:
            # Gestion des erreurs lors de la connexion à MariaDB
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)  # Sortie du programme avec un code d'erreur 1 en cas d'échec de connexion

    def close(self):
        # Méthode pour fermer la connexion à la base de données
        if self.conn:
            self.conn.close()

    def DQL(self, requete: str, params: tuple = ()):
        """
        Méthode pour les requêtes de sélection (SELECT)
        Returns a list of dictionaries representing the query results
        """
        try:
            self.cursor.execute(requete, params)
            return self.cursor.fetchall()
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def DML(self, requete: str, params: tuple = ()):
        """
        Méthode pour les requêtes de modification (INSERT, UPDATE, DELETE)
        """
        try:
            self.cursor.execute(requete, params)
            self.conn.commit()  # Commit the transaction
            return self.cursor.rowcount  # Retourne le nombre de lignes affectées
        except mariadb.Error as e:
            print(f"Error MariaDB: {e}")
            self.conn.rollback()  # Rollback the transaction in case of error
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Créer une instance globale de Database pour être utilisée dans toute l'application
db = Database()
