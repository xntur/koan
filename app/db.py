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


# Everything below just sets up the databases.        
create_sql_teams_table = """
  CREATE TABLE IF NOT EXISTS dependencies (
    id integer PRIMARY KEY,
    name text NOT NULL,
    points integer
  );"""
create_sql_answered_table = """
  CREATE TABLE IF NOT EXISTS answered (
    team_id integer NOT NULL,
    question_id integer NOT NULL,
    PRIMARY KEY (team_id, question_id)
  );"""
create_sql_questions_table = """
  CREATE TABLE IF NOT EXISTS questions (
    id integer PRIMARY KEY,
    name text NOT NULL,
    question text NOT NULL,
    count integer NOT NULL,
    points integer NOT NULL
  );"""
create_sql_dependencies_table = """
  CREATE TABLE IF NOT EXISTS questions (
    solve_first integer NOT NULL,
    solve_next integer NOT NULL,
    PRIMARY KEY (solve_first, solve_next)
  );"""
@app.before_first_request
def maybe_create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute(create_sql_teams_table)
    c.execute(create_sql_dependencies_table)
    c.execute(create_sql_questions_table)
    c.execute(create_sql_answered_table)
    conn.commit()
