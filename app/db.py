from app import app
from flask import g
import sqlite3
import os
import json

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
    id text PRIMARY KEY,
    name text NOT NULL,
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
            questions(id,name,question,answer,count,points)
            VALUES(?,?,?,?,?,?)'''
    dependencies_sql = '''
        INSERT OR REPLACE INTO
            dependencies(solve_first, solve_next)
            VALUES(?,?)'''
    for filename in os.listdir(root):
        if filename.endswith('.questionfile'):
            fp = open(root + filename, 'r')
            id = filename.split('.')[0]
            name = fp.readline()
            question = fp.readline()
            answer = fp.readline()
            points = fp.readline()
            deps = fp.readline().split(',')
            c.execute(question_sql, (id.rstrip(),
                                     name.rstrip(),
                                     question.rstrip(),
                                     answer.rstrip(),
                                     0,
                                     points))
            for dep in deps:
                if len(dep.rstrip()) != 0:
                    c.execute(dependencies_sql, (dep.rstrip(), id.rstrip()))
            fp.close()
    conn.commit()

def question(data):
    return {
        'id': data[0],
        'name': data[1],
        'question': data[2],
        'answer': data[3],
        'count': data[4],
        'points': data[5],
    }

def questions():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    questions = c.fetchall()
    out = []
    for data in questions:
        out.append(question(data))
    return out

def getquestion(questionid):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM questions WHERE id = ?', [questionid])
    return question(c.fetchall()[0])

def dependencies():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM dependencies')
    deps = c.fetchall()
    questionToDeps = {}
    for dep in deps:
        if dep[1] not in questionToDeps:
            questionToDeps[dep[1]] = []
        questionToDeps[dep[1]].append(dep[0])
    return questionToDeps

def getpoints(team):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM teams WHERE name = ?', [team])
    teams = c.fetchall()
    points = 0
    if len(teams) == 1:
        points = teams[0][1]
    return points

def getanswered(team):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM answered WHERE team = ?', [team])
    return set([i[1] for i in c.fetchall()])

def correct(team, question):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM answered WHERE team = ? AND question = ?',
              [team, question['id']])
    answered = c.fetchall()
    if len(answered) == 0:
        c.execute('SELECT * FROM teams WHERE name = ?', [team])
        teams = c.fetchall()
        points = 0
        if len(teams) == 1:
            points = teams[0][1]
        c.execute('INSERT OR REPLACE INTO answered(team,question) VALUES(?,?)',
                  [team, question['id']])
        c.execute('INSERT OR REPLACE INTO teams(name,points) VALUES(?,?)',
                  [team, question['points'] + points])
    conn.commit()
