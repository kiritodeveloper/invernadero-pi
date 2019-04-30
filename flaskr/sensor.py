impo#rt functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('sensor', __name__, url_prefix='/sensor')
datatypes = ["integer","real","datetime"]

@bp.route('/index')
def index():
    db = get_db()
    sensors = db.execute(
            'SELECT se.id as id, se.name as name, site_id, si.name as sname'
        ' FROM sensor se JOIN site si ON se.site_id = si.id'
        ' ORDER BY se.id DESC'
    ).fetchall()
    return render_template('sensor/index.html', sensors=sensors)


@bp.route('/create', methods=('GET', 'POST'))
def create():

    db = get_db()
    lugares = db.execute(
        'SELECT id, name, description'
        ' FROM site'
        ' ORDER BY id DESC'
    ).fetchall()
 
    if request.method == 'POST':

        name = request.form['name']
        lugar = request.form['lugar']
        datatype = request.form['datatype']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del sensor es requerido.'
        elif (' ' in name):
              error = 'El nombre no debe llevar espacios'
        elif db.execute(
            'SELECT id FROM sensor WHERE name = ? AND site_id = ?', (name,lugar)
        ).fetchone() is not None:
            error = 'El sensor {} ya existe.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO sensor (name, site_id,datatype) VALUES (?, ?, ?)',
                (name, lugar, datatype)
            )
            lugarnombre = db.execute('SELECT name FROM site WHERE id = ? ', (lugar)).fetchone()
            db.execute (
                'ALTER TABLE sitetable'+lugarnombre[0]+' ADD COLUMN '+name+' '+ datatype
            )
            db.commit()
            return redirect(url_for('sensor.index'))

        flash(error)


    return render_template('sensor/crear.html',lugares=lugares, datatypes=datatypes)


def get_sensor(id):
    sensor = get_db().execute(
        'SELECT id, name, site_id, datatype'
        ' FROM sensor '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if sensor is None:
        abort(404, "El id del sensor {0} no existe.".format(id))

    return sensor

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    sensor = get_sensor(id)

    db = get_db()
    lugares = db.execute(
        'SELECT id, name, description'
        ' FROM site'
        ' ORDER BY id DESC'
    ).fetchall()


    return render_template('sensor/update.html', sensor=sensor,lugares=lugares,datatypes=datatypes)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    #Obtenemos los campos de los datos que queremos eliminar
    sensor = get_sensor(id)
   
    db = get_db()
    
    #Para borrar el sensor, necesitamos borrar la columna de la tabla sitetable"lugarr"
    #Para ello renombramos la tabla, creamos de nuevo la tabla sin la columna a borrar
    #pasamos los datos y borramos la tabla temporal y borramos el registro en la tabla sensor
    tablatemporal='temporal'
    tabla = db.execute('SELECT name FROM site WHERE id='+str(sensor['site_id'])).fetchone()
    columnas = db.execute('SELECT name, datatype FROM sensor WHERE site_id='+str(sensor['site_id']))

    #Renombramos la tabla actual a una temporal
    db.execute('ALTER TABLE sitetable'+tabla['name']+' RENAME TO '+tablatemporal)

    #Creamos la tabla inicial
    db.execute('CREATE TABLE sitetable'+tabla['name']+'( id INTEGER PRIMARY KEY AUTOINCREMENT )')

    campos = ''
    for columna in columnas:
        if columna['name'] != sensor['name']:
            #Recreamos las columnas en la nueva tabla, menos la que se va a borrar
            db.execute('ALTER TABLE sitetable'+tabla['name']+' ADD COLUMN '+columna['name']+' '+columna['datatype'])
            campos =campos+columna['name']+','
    #Quitamos la ultima coma de la lista de columnas
    campos=campos[:-1]

    #insertamos los campos de la tabla anterior a la nueva
    db.execute('INSERT INTO sitetable'+tabla['name']+' SELECT id,'+campos+' FROM '+tablatemporal)
    
    #Borramos el reistro de la tabla sensor
    db.execute('DELETE FROM sensor WHERE id = ?', (id,))

    #Borramos la tabla temporal
    db.execute('DROP TABLE '+tablatemporal)
    
    db.commit()
    return redirect(url_for('sensor.index'))
