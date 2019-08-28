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
create_sql_questions_table = """
  CREATE TABLE IF NOT EXISTS questions (
    name text PRIMARY KEY,
    question text NOT NULL,
    answer text NOT NULL,
    count integer NOT NULL,
    points integer NOT NULL
  );"""

create_sql_teams_table = """
  CREATE TABLE IF NOT EXISTS teams (
    name text PRIMARY KEY,
    points integer
  );"""

create_sql_answered_table = """
  CREATE TABLE IF NOT EXISTS answered (
    team text NOT NULL,
    question text NOT NULL,
    PRIMARY KEY (team, question)
  );"""

create_sql_dependencies_table = """
  CREATE TABLE IF NOT EXISTS dependencies (
    solve_first text NOT NULL,
    solve_next text NOT NULL,
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

    add_questions()

def add_questions():
    conn = get_db()
    c = conn.cursor()
    root = 'app/questions/'
    question_sql = '''
        INSERT OR REPLACE INTO 
            questions(name,question,answer,count,points)
            VALUES(?,?,?,?,?)'''
    dependencies_sql = '''
        INSERT OR REPLACE INTO
            dependencies(solve_first, solve_next)
            VALUES(?,?)'''
    for filename in os.listdir(root):
        if filename.endswith('.questionfile'):
            fp = open(root + filename, 'r')
            name = fp.readline()
            question = fp.readline()
            answer = fp.readline()
            points = fp.readline()
            deps = fp.readline().split(',')
            c.execute(question_sql, (name, question, answer, 0, points))
            for dep in deps:
                c.execute(dependencies_sql, (dep, name))
            fp.close()
    conn.commit()
