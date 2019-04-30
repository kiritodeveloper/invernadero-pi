import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('site', __name__, url_prefix='/site')

@bp.route('/index')
def index():
    db = get_db()
    sites = db.execute(
        'SELECT id, name, description'
        ' FROM site'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('site/index.html', sites=sites)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del lugar es requerido.'
        elif (' ' in name):
              error = 'El nombre no debe llevar espacios'
        elif not description:
            error = 'La descripción es requerida'
        elif db.execute(
            'SELECT id FROM site WHERE name = ?', (name.lower(),)
        ).fetchone() is not None:
            error = 'El lugar {} ya existe.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO site (name, description) VALUES (?, ?)',
                (name.lower(), description)
            )
            db.execute (
                'CREATE TABLE sitetable'+name.lower()+'  ( id INTEGER PRIMARY KEY AUTOINCREMENT )'
            )
            db.commit()
            return redirect(url_for('site.index'))

        flash(error)


    return render_template('site/crear.html')


def get_site(id):
    site = get_db().execute(
        'SELECT id, name, description'
        ' FROM site '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if site is None:
        abort(404, "El id del lugar {0} no existe.".format(id))

    return site

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    site = get_site(id)

    if request.method == 'POST':
        description = request.form['description']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE site SET  description = ?'
                ' WHERE id = ?',
                (description, id)
            )
            db.commit()
            return redirect(url_for('site.index'))

    return render_template('site/update.html', site=site)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    #Obtenemos los campos de los datos que queremos eliminar
    site = get_site(id)
    db = get_db()
    #Borramos el reistro de la tabla site
    db.execute('DELETE FROM site WHERE id = ?', (id,))
    #Buscamos la tabla para eliminarla
    db.execute('DROP TABLE sitetable'+site[1])
    db.commit()
    return redirect(url_for('site.index'))
