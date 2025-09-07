from fastapi import HTTPException
import mariadb
import sys
import traceback


# Définition de la classe Database pour gérer la connexion à la base de données MariaDB
class Database:
    def __init__(self):
        try:
            # Tentative de connexion à la base de données MariaDB
            self.conn = mariadb.connect(
                user="root",             # Nom d'utilisateur pour se connecter à la base de données
                password="root",         # Mot de passe pour se connecter à la base de données
                host="db",        # Adresse IP de l'hôte de la base de données (localhost)
                port=3306,               # Port utilisé pour la connexion à la base de données MariaDB
                database="bd_projet_AIS"  # Nom de la base de données à laquelle se connecter
            )
            # Création d'un curseur pour exécuter des requêtes SQL
            self.cursor = self.conn.cursor(dictionary=True)
        except mariadb.Error as e:
            # Gestion des erreurs lors de la connexion à MariaDB
            print(f"Error connecting to MariaDB Platform: {e}")
            traceback.print_exc()
            sys.exit(1)  # Sortie du programme avec un code d'erreur 1 en cas d'échec de connexion

    def close(self):
        # Méthode pour fermer la connexion à la base de données
        if self.conn:
            self.conn.close()
    
    def DQL(self, requete: str, params: tuple = ()):
        result_list = []
        try:
            self.cursor.execute(requete, params)
            columns = [col[0] for col in self.cursor.description]
            for row in self.cursor:
                row_dict = {columns[i]: row[i] for i in range(len(columns))}
                result_list.append(row_dict)
            return result_list
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    def DML(self, requete: str, params: tuple = ()):
        try:
            self.cursor.execute(requete, params)
            self.conn.commit()  # Commit the transaction
        except mariadb.Error as e:
            print(f"Error MariaDB: {e}")
            self.conn.rollback()  # Rollback the transaction in case of error
            sys.exit(1)






