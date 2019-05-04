import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from piinvernadero.auth import login_required
from piinvernadero.db import get_db

bp = Blueprint('actuator', __name__, url_prefix='/actuator')

@bp.route('/index')
@login_required
def index():
    db = get_db()
    actuators = db.execute(
        'SELECT ac.id as id, ac.name as name, status, sensor_id, se.name as sensor, si.name as site'
        ' FROM actuator ac JOIN sensor se ON ac.sensor_id=se.id '
        ' JOIN site si ON se.site_id=si.id'
        ' ORDER BY id ASC'
    ).fetchall()

    return render_template('actuator/index.html', actuators=actuators)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    sensores = db.execute(
        'SELECT se.id as id, se.name as name, site_id, si.name as site'
        ' FROM  sensor se JOIN site si ON se.site_id=si.id'
        ' ORDER BY si.id,se.id ASC'
    ).fetchall()


    if request.method == 'POST':
        name = request.form['name']
        sensor_id = request.form['sensor_id']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del actuador es requerido.'
        elif db.execute(
            'SELECT id FROM actuator WHERE name = ?', (name,)
        ).fetchone() is not None:
            error = 'El actuator {} ya existe.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO actuator (name,status,sensor_id) VALUES (?, 0, ?)',
                (name, sensor_id)
            )
            db.commit()
            return redirect(url_for('actuator.index'))

        flash(error)

    return render_template('actuator/crear.html', sensores=sensores)


def get_actuator(id):
    actuator = get_db().execute(
        'SELECT id, name, status, sensor_id'
        ' FROM actuator '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if actuator is None:
        abort(404, "El actuator id {0} no existe.".format(id))

    return actuator

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    actuator = get_actuator(id)

    db = get_db()
    sensores = db.execute(
        'SELECT se.id as id, se.name as name, site_id, si.name as site'
        ' FROM  sensor se JOIN site si ON se.site_id=si.id'
        ' ORDER BY si.id,se.id ASC'
    ).fetchall()


    if request.method == 'POST':
        name = request.form['name']
        sensor_id = request.form['sensor_id']
        if request.form.get('status'):
            status=1
        else:
            status=0

        error = None

        if not name:
            error = 'El nombre es requerido.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE actuator SET name = ?, sensor_id = ?, status= ?'
                ' WHERE id = ?',
                (name, sensor_id, status, id)
            )
            db.commit()
            return redirect(url_for('actuator.index'))

    return render_template('actuator/update.html', actuator=actuator, sensores=sensores)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_actuator(id)
    db = get_db()
    db.execute('DELETE FROM actuator WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('actuator.index'))
