#!/bin/bash
set -e

# Démarrer MariaDB en arrière-plan
mysqld_safe &

# Attendre que MariaDB soit prêt avec une requête SQL
until mariadb -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1;" > /dev/null 2>&1; do
  echo "⏳ Attente de MariaDB..."
  sleep 1
done

echo "✅ MariaDB est prêt !"

# Exécuter la commande principale
exec "$@"

