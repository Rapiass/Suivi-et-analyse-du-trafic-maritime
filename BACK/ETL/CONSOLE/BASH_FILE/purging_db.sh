#!/bin/bash

# Path to the .env file containing credentials
CREDENTIALS_FILE="./db_info.env"

# Check if the credentials file exists
if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "Error: Credentials file '$CREDENTIALS_FILE' not found."
  exit 1
fi

# Load database credentials from the .env file
source "$CREDENTIALS_FILE"

# Ensure the database is provided
if [ -z "$DB_NAME" ]; then
  echo "Error: Database name is not provided in the credentials file."
  exit 1
fi

# MySQL connection test
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "quit" &>/dev/null
if [ $? -ne 0 ]; then
  echo "Error: Could not connect to the MySQL server. Please check your credentials."
  exit 1
fi

mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "DROP SCHEMA $DB_NAME;"

echo "Database purge completed. All tables in '$DB_NAME' are emptied."
