import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from piinvernadero.auth import login_required
from piinvernadero.db import get_db

bp = Blueprint('grupo', __name__, url_prefix='/grupo')

@bp.route('/index')
@login_required
def index():
    db = get_db()
    grupos = db.execute(
        'SELECT id, name, description'
        ' FROM grupo'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('grupo/index.html', grupos=grupos)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del grupo es requerido.'
        elif not description:
            error = 'La descripción es requerida'
        elif db.execute(
            'SELECT id FROM grupo WHERE name = ?', (name,)
        ).fetchone() is not None:
            error = 'El grupo {} ya existe.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO grupo (name, description) VALUES (?, ?)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('grupo.index'))

        flash(error)

    return render_template('grupo/crear.html')


def get_grupo(id):
    grupo = get_db().execute(
        'SELECT id, name, description'
        ' FROM grupo '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if grupo is None:
        abort(404, "El grupo id {0} no existe.".format(id))

    return grupo

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    grupo = get_grupo(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        error = None

        if not name:
            error = 'El nombre es requerido.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE grupo SET name = ?, description = ?'
                ' WHERE id = ?',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('grupo.index'))

    return render_template('grupo/update.html', grupo=grupo)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_grupo(id)
    db = get_db()
    db.execute('DELETE FROM grupo WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('grupo.index'))
