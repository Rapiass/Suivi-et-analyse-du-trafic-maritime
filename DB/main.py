from Database import Database  # Importer la classe Database depuis le dossier DB

# Connexion à la base de données via Database.py
def connect_to_db():
    db = Database()  # Créer une instance de la classe Database pour se connecter à la base de données
    return db

# Exécution du fichier SQL pour initialiser la base de données
def execute_sql_script(db, script_path):
    with open(script_path, 'r') as sql_file:
        sql_script = sql_file.read()
    
    try:
        db.DML(sql_script)  # Utilisation de la méthode DML pour exécuter le script SQL
        print("SQL script executed successfully!")
    except Exception as e:
        print(f"Error executing SQL script: {e}")

# Fonction principale
def main():
    # Connexion à la base de données via Database.py
    db = connect_to_db()

    # Exécution du script SQL pour initialiser la base de données
    execute_sql_script(db, '/app/BD.sql')

    # Fermer la connexion à la base de données
    db.close()

if __name__ == '__main__':
    main()

