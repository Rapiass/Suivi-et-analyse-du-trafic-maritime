#!/bin/bash

# Path to the .env file containing credentials
CREDENTIALS_FILE="./ETL/db_info.env"

# Check if the credentials file exists
if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "Error: Credentials file '$CREDENTIALS_FILE' not found."
  exit 1
fi

# Load database credentials from the .env file
source "$CREDENTIALS_FILE"

# Export directory
EXPORT_DIR="./ETL/TEMP/CSV_BACKUP/"

# Ensure the export directory exists
mkdir -p "$EXPORT_DIR"

# Tables to export
TABLES=("User" "UserHasRole" "UserHasVessel" "Company")

# Loop through each table and export
for TABLE in "${TABLES[@]}"; do
  FILE_NAME="${EXPORT_DIR}${TABLE}.csv"
  echo "Exporting table: $TABLE to $FILE_NAME"

  {
    # Print the header row once
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "SHOW COLUMNS FROM $TABLE;" | \
    awk 'NR > 1 { print $1 }' | paste -sd ',' -

    # Print the table data, skipping the first row (which is the column header)
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "SELECT * FROM $TABLE;" | \
    tail -n +2 | sed 's/\t/,/g'
  } > "$FILE_NAME"

  if [ $? -eq 0 ]; then
    echo "Successfully exported $TABLE to $FILE_NAME"
  else
    echo "Failed to export $TABLE to $FILE_NAME"
  fi
done
