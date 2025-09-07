#!/bin/bash

#Pour ce fichier 
#./create_db -f {le script SQL}

# Path to the .env file containing credentials
CREDENTIALS_FILE="./db_info.env"

# SQL file path
SQL_FILE="./TEMP/STATIC/BD.sql"

# Check if the credentials file exists
if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "Error: Credentials file '$CREDENTIALS_FILE' not found."
  exit 1
fi

# Load database credentials from the .env file
source "$CREDENTIALS_FILE"

# Check if the SQL file exists
if [ ! -f "$SQL_FILE" ]; then
  echo "Error: SQL file '$SQL_FILE' not found."
  exit 1
fi

# Execute the SQL file
mysql -u "$DB_USER" -p"$DB_PASS" -h "$DB_HOST" < "$SQL_FILE"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "SQL file executed successfully."
else
  echo "Error: Failed to execute SQL file."
fi