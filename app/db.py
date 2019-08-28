from app import app
from flask import g
import sqlite3
import os

DATABASE = os.environ.get('KOAN_DB_PATH')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_first_request
def maybe_create_tables():
    if len(get_db().execute('SELECT * FROM sqlite_master WHERE type="table"').fetchall()) == 0:
        

    
