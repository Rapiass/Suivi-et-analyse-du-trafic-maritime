#!/bin/bash

SOURCE_DB="bd_projet_AIS"
STORAGE_DB="bd_stockage"
DB_USER="test_user" 
DB_PASSWORD="test_password"
DB_HOST="db_cont"

# Dump de la base de données source
echo "Dumping la base de données $SOURCE_DB..."
mysqldump -u$DB_USER -p$DB_PASSWORD -h$DB_HOST $SOURCE_DB > "dump.sql"

# Création de la base de données de stockage si elle n'existe pas
echo "Création de la base de données de stockage $STORAGE_DB si elle n'existe pas..."
mysql -u$DB_USER -p$DB_PASSWORD -h$DB_HOST -e "CREATE DATABASE IF NOT EXISTS $STORAGE_DB;"

# Restauration dans la base de stockage
echo "Restauration du dump dans la base de stockage $STORAGE_DB..."
mysql -u$DB_USER -p$DB_PASSWORD -h$DB_HOST $STORAGE_DB < "dump.sql"

# Suppression du fichier temporaire de dump
rm "dump.sql"

echo "Dump et restauration terminés."
