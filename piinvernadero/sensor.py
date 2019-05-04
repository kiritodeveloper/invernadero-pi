import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from piinvernadero.auth import login_required
from piinvernadero.db import get_db

bp = Blueprint('sensor', __name__, url_prefix='/sensor')
datatypes = ["integer","real","datetime"]


#Muestra los sensores con todos sus datos listados
@bp.route('/index')
@login_required
def index():
    db = get_db()
    sensors = db.execute(
            'SELECT se.id as id, se.name as name, site_id, si.name as sname, unit, min, max'
        ' FROM sensor se JOIN site si ON se.site_id = si.id'
        ' ORDER BY si.id,se.id ASC'
    ).fetchall()
    return render_template('sensor/index.html', sensors=sensors)

#Muestra la grafica de un sensor
@bp.route('/<int:id>/graph', methods=('GET', 'POST'))
@login_required
def graph(id):
    sensor = get_sensor(id)

    db = get_db()
    lugar = db.execute(
        'SELECT id, name, description'
        ' FROM site WHERE id='+str(sensor['site_id'])+
        ' ORDER BY id DESC'
    ).fetchone()

    return render_template('sensor/graph.html', lugar=lugar, sensor=sensor)


#Crea un sensor
@bp.route('/create', methods=('GET', 'POST'))
@login_required
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
        unit = request.form['unit']
        min = request.form['min']
        max = request.form['max']
        db = get_db()
        error = None

        if not name:
            error = 'El nombre del sensor es requerido.'
        elif not unit:
              error = 'La unidad del sensor es requerido'
        elif not min:
              error = 'El sensor debe tener un valor mínimo'
        elif not max:
              error = 'El sensor debe tener un valor máximo'
        elif (' ' in name):
              error = 'El nombre no debe llevar espacios'
        elif db.execute(
            'SELECT id FROM sensor WHERE name = ? AND site_id = ?', (name,lugar)
        ).fetchone() is not None:
            error = 'El sensor {} ya existe.'.format(name)
        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO sensor (name, site_id,datatype,unit,min,max) VALUES (?, ?, ?, ?, ?, ?)',
                (name, lugar, datatype, unit, min, max)
            )
            lugarnombre = db.execute('SELECT name FROM site WHERE id = ? ', (lugar)).fetchone()
            db.execute (
                'ALTER TABLE sitetable'+lugarnombre[0]+' ADD COLUMN '+name+' '+ datatype
            )
            db.commit()
            return redirect(url_for('sensor.index'))
    return render_template('sensor/crear.html',lugares=lugares, datatypes=datatypes)


#Obtiene datos de un sensor
def get_sensor(id):
    sensor = get_db().execute(
        'SELECT id, name, site_id, datatype, unit, min, max'
        ' FROM sensor '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if sensor is None:
        abort(404, "El id del sensor {0} no existe.".format(id))

    return sensor

#Actualiza (solo Borra) un sensor
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


#Borra un sensor y su columna asignada
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    #Obtenemos los campos de los datos que queremos eliminar
    sensor = get_sensor(id)
    
    db = get_db()
    error = None

    if db.execute(
            'SELECT id FROM actuator WHERE sensor_id = '+str(id)
        ).fetchone() is not None:
            error = 'El sensor {} tiene actuadores asociados. Debe borrar los actuadores asociados antes de borrar.'.format(sensor['name'])
    if error is not None:
            flash(error)
    else:
        #Para borrar el sensor, necesitamos borrar la columna de la tabla sitetable"lugarr"
        #Para ello renombramos la tabla, creamos de nuevo la tabla sin la columna a borrar
        #pasamos los datos y borramos la tabla temporal y borramos el registro en la tabla sensor
        tablatemporal='temporal'
        tabla = db.execute('SELECT name FROM site WHERE id='+str(sensor['site_id'])).fetchone()
        columnas = db.execute('SELECT name, datatype FROM sensor WHERE site_id='+str(sensor['site_id']))

        #Renombramos la tabla actual a una temporal
        print ('ALTER TABLE sitetable'+tabla['name']+' RENAME TO '+tablatemporal)
        db.execute('ALTER TABLE sitetable'+tabla['name']+' RENAME TO '+tablatemporal)

        #Creamos la tabla inicial
        print ('CREATE TABLE sitetable'+tabla['name']+'( id INTEGER PRIMARY KEY AUTOINCREMENT, date datetime )')
        db.execute('CREATE TABLE sitetable'+tabla['name']+'( id INTEGER PRIMARY KEY AUTOINCREMENT, date datetime )')

        campos = ''
        for columna in columnas:
            if columna['name'] != sensor['name']:
                #Recreamos las columnas en la nueva tabla, menos la que se va a borrar
                print('ALTER TABLE sitetable'+tabla['name']+' ADD COLUMN '+columna['name']+' '+columna['datatype'])
                db.execute('ALTER TABLE sitetable'+tabla['name']+' ADD COLUMN '+columna['name']+' '+columna['datatype'])
                campos =campos+columna['name']+','
        #Quitamos la ultima coma de la lista de columnas
        campos=campos[:-1]

        #insertamos los campos de la tabla anterior a la nueva
        if campos != '':
            print('INSERT INTO sitetable'+tabla['name']+' SELECT id,date,'+campos+' FROM '+tablatemporal)
            db.execute('INSERT INTO sitetable'+tabla['name']+' SELECT id,date,'+campos+' FROM '+tablatemporal)

        #Borramos el reistro de la tabla sensor
        print('DELETE FROM sensor WHERE id = ?', (id,))
        db.execute('DELETE FROM sensor WHERE id = ?', (id,))

        #Borramos la tabla temporal
        print('DROP TABLE '+tablatemporal)
        db.execute('DROP TABLE '+tablatemporal)
    
        db.commit()
        
    return redirect(url_for('sensor.index'))
