from functools import wraps
import sqlite3
import os
import click
from flask import current_app, g
import logging

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

def use_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = get_db()
        cursor = db.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            db.commit()
            return result
        except ValueError as e:
            db.rollback()
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e
        finally:
            close_db()
    return wrapper

def init_db():
    db = get_db()

    schema_path = current_app.root_path + '/schema.sql'
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    logging.info("Database initialized.")

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)