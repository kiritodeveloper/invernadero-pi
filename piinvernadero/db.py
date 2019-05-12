import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


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

def init_db():
    db = get_db()

    #Para borrar las tablas que se crearon en la programacion NOTA: Se puede optimizar el codigo
    dropstring = []
    c = db.cursor()
    #Generando las sentencias SQL de DROP TABLE
    for row in c.execute(
        'select "DROP TABLE IF EXISTS " || name || ";" FROM sqlite_master WHERE type = "table" AND name LIKE "sitetable%"'
    ):
        dropstring.append( row[0])
    #Ejecutando las sentencias
    for row in dropstring:
        print ("Borrando con %s " % (row))
        c.execute(row)
   #Guardando cambios
    db.commit()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

