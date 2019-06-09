import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from piinvernadero.auth import login_required
from piinvernadero.db import get_db

bp = Blueprint('site', __name__, url_prefix='/site')

@bp.route('/index')
@login_required
def index():
    db = get_db()
    sites = db.execute(
        'SELECT id, name, address, description'
        ' FROM site'
        ' ORDER BY id ASC'
    ).fetchall()

    sensores = db.execute(
        'SELECT id, name, site_id'
        ' FROM sensor'
        ' ORDER BY id ASC'
    ).fetchall()

    return render_template('site/index.html', sites=sites, sensores=sensores)


#Muestra las graficas de un lugar
@bp.route('/<int:id>/graph', methods=('GET', 'POST'))
@login_required
def graph(id):
    lugar = get_site(id)

    db = get_db()
    sensores = db.execute(
        'SELECT id, name, site_id, unit, min, max'
        ' FROM sensor WHERE site_id='+str(lugar['id'])+
        ' ORDER BY id DESC'
    ).fetchall()

    return render_template('site/graph.html', lugar=lugar, sensores=sensores)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del lugar es requerido.'
        elif (' ' in name):
              error = 'El nombre no debe llevar espacios'
        elif (' ' in address):
              error = 'La direccion del lugar es requerido'
        elif not description:
            error = 'La descripción es requerida'
        elif db.execute(
            'SELECT id FROM site WHERE name = ?', (name.lower(),)
        ).fetchone() is not None:
            error = 'El lugar {} ya existe.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO site (name, address, description) VALUES (?, ?, ?)',
                (name.lower(), address, description)
            )
            db.execute (
                'CREATE TABLE sitetable'+name.lower()+'  ( id INTEGER PRIMARY KEY AUTOINCREMENT, date datetime )'
            )
            db.commit()
            return redirect(url_for('site.index'))

        flash(error)


    return render_template('site/crear.html')

def get_site(id):
    site = get_db().execute(
        'SELECT id, name, address, description'
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
        address = request.form['address']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE site SET  address=?,description = ?'
                ' WHERE id = ?',
                (address, description, id)
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

    error = None
    if db.execute(
            'SELECT id FROM sensor WHERE  site_id = '+str(id)
        ).fetchone() is not None:
            error = 'El lugar {} aun tiene asociados sensores.'.format(site[1])
    if error is None:
        #Borramos todos los sensores que pertenezcan al lugar
        #db.execute('DELETE FROM sensor WHERE site_id = ?', (id,))
        #Borramos el reistro de la tabla site
        db.execute('DELETE FROM site WHERE id = ?', (id,))
        #Buscamos la tabla para eliminarla
        db.execute('DROP TABLE sitetable'+site[1])
        db.commit()
        return redirect(url_for('site.index'))
    flash(error)
    return redirect(url_for('site.index'))
