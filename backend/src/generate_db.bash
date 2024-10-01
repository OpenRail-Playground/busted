#!/bin/bash

# Database file
mkdir -p instance
DB_FILE="instance/busted.db"

# Directories containing CSV files
directories=("resources/data/current" "resources/data/previous")

# Loop through all directories
for dir in "${directories[@]}"; do
    dir_name=$(basename "$dir")
    # Loop through all CSV files in the directory
    for file in "$dir"/*.txt; do
        # Get the base name of the file (without path and extension)
        file_name=$(basename "$file" .txt)
        table_name="${dir_name}_${file_name}"
        # Import the CSV file into the SQLite database
        sqlite3 "$DB_FILE" <<EOF
.mode csv
.import "$file" "$table_name"
EOF
    done
done

