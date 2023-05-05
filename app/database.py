import sqlite3
from flask import Flask, current_app, g
from app import app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db

def first_init():
    with g.open_resource('schema.sql') as f:
        commands = f.read().decode('utf-8').split(';')
        db = get_db()
        for command in commands:
            db.execute(command)
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()