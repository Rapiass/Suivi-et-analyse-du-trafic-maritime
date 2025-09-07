#!/bin/bash

# Pour ce fichier 
# ./sql_file -f {le script SQL}

CREDENTIALS_FILE="./ETL/db_info.env"

# Vérifie si le fichier des credentials existe
if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "Error: Credentials file '$CREDENTIALS_FILE' not found."
  exit 1
fi

# Charge les credentials de la base de données
source "$CREDENTIALS_FILE"

# Requête SQL par défaut
DEFAULT_SQL_QUERY="SELECT 1 FROM DUAL LIMIT 1;"

# Montre l'usage de la base de données
usage() {
  echo "Usage: $0 [-f sql_file]"
  echo "  -f sql_file  Specify an SQL file to execute on the database"
  exit 1
}

# Lit la ligne de commande pour récupérer un fichier
while getopts "f:" opt; do
  case ${opt} in
    f )
      SQL_FILE=$OPTARG
      ;;
    \? )
      usage
      ;;
  esac
done

# Vérifie si un fichier SQL est fourni et accessible
if [ -n "$SQL_FILE" ]; then
  if [ ! -f "$SQL_FILE" ]; then
    echo "Error: File '$SQL_FILE' not found."
    exit 1
  fi
else
  # Utilise la requête par défaut
  echo "No SQL file provided, using default query."
  mysql -u "$DB_USER" -p"$DB_PASS" -h "$DB_HOST" -D "$DB_NAME" -e "$DEFAULT_SQL_QUERY"
  exit 0
fi

# Execute the SQL file
mysql -u "$DB_USER" -p"$DB_PASS" -h "$DB_HOST" -D "$DB_NAME" < "$SQL_FILE"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "SQL file executed successfully."
else
  echo "Error: Failed to execute SQL file."
fi
