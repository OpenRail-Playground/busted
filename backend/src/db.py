import sqlite3
import os
import glob
import csv

import click
from flask import current_app, g

# Initialise the database based on the schema.sql file
def init_db():
    db = get_db()

    # Execute schema.sql script
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # Create tables based on CSV headers
    create_tables(db)

# Function to create tables based on CSV headers
def create_tables(db):
    # Directories containing CSV files
    directories = ["resources/data/current", "resources/data/previous"]

    for dir in directories:
        dir_name = os.path.basename(dir)
        for file in glob.glob(os.path.join(dir, '*.txt')):
            file_name = os.path.splitext(os.path.basename(file))[0]
            table_name = f"{dir_name}_{file_name}"
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                columns = ', '.join([f'"{col}" TEXT' for col in header])
                db.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')
            print(f"Created table {table_name} based on {file}")
                        
# Function to insert data into tables from CSV files
def insert_data():
    db = get_db()
    directories = ["resources/data/current", "resources/data/previous"]

    for dir in directories:
        dir_name = os.path.basename(dir)
        for file in glob.glob(os.path.join(dir, '*.txt')):
            file_name = os.path.splitext(os.path.basename(file))[0]
            table_name = f"{dir_name}_{file_name}"
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header row
                placeholders = ','.join('?' * len(next(reader)))
                rows = []
                for row in reader:
                    rows.append(row)
                db.executemany(
                    f'INSERT INTO "{table_name}" VALUES ({placeholders})',
                    rows
                )
            print(f"Inserted data from {file} into table {table_name}")
            
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database and seeded with init values.')
    
@click.command('insert-data')
def insert_data_command():
    """Insert data into tables from CSV files."""
    insert_data()
    click.echo('Inserted data into tables from CSV files.')

# add the close_db function and the init_db_command to the app context
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_data_command)
    