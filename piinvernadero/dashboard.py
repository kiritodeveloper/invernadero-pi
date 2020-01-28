import functools
import datetime
import time
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from piinvernadero.auth import login_required
from piinvernadero.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
datatypes = ["integer","real","datetime"]

@bp.route('/index')
@login_required
def index():
    db = get_db()
    sensores = db.execute(
        'SELECT id, name, site_id, unit, min, max'
        ' FROM sensor '
        ' ORDER BY id ASC'
    ).fetchall()
    lugares = db.execute(
        'SELECT id, name'
        ' FROM site '
        ' ORDER BY id ASC'
    ).fetchall()

    actuators = db.execute(
        'SELECT ac.id as id, ac.name as name, status, sensor_id, se.name as sensor, si.name as site'
        ' FROM actuator ac JOIN sensor se ON ac.sensor_id=se.id '
        ' JOIN site si ON se.site_id=si.id'
        ' ORDER BY id ASC'
    ).fetchall()


    #print (*lugares,sep = ", ")
    #print (lugares[0]['id'])
    return render_template('dashboard/index.html', sensores=sensores,lugares=lugares, actuators=actuators)

@bp.route('/actual')
@login_required
def actual():
    db = get_db()
    sensores = db.execute(
            'SELECT id, name, site_id'
        ' FROM sensor '
        ' ORDER BY id ASC'
    ).fetchall()
    lugares = db.execute(
            'SELECT id, name'
        ' FROM site '
        ' ORDER BY id ASC'
    ).fetchall()
    return render_template('dashboard/actual.html', sensores=sensores,lugares=lugares)


@bp.route('/<int:id>/<int:sensor>/gaugejson')
@login_required
def gaugejson(id,sensor):
    db = get_db()

    tabla = db.execute('SELECT name FROM site WHERE id='+str(id)).fetchone()
    namesensor = db.execute('SELECT name FROM sensor WHERE id='+str(sensor)).fetchone()
    #Falta mandar error cuando no encuentra el sensor
    resultado = db.execute(
            'SELECT '+namesensor['name']+
            ' FROM sitetable'+tabla['name']+
        ' ORDER BY date DESC LIMIT 1'
    ).fetchone()
    #print (resultado[namesensor['name']])
    return str(resultado[namesensor['name']])




@bp.route('/<int:id>/<int:sensor>/datajson')
@login_required
def datajson(id,sensor):
    db = get_db()

    tabla = db.execute('SELECT name FROM site WHERE id='+str(id)).fetchone()
    namesensor = db.execute('SELECT name FROM sensor WHERE id='+str(sensor)).fetchone()
    #print (namesensor['name'])
    #Falta mandar error cuando no encuentra el sensor
    resultados = db.execute(

           'SELECT strftime("%s",substr(date,0,5)||"-" ||substr(date,5,2)||"-"||substr(date,7,2)||" "||substr(date,9,2)||":"||substr(date,11,2)||":"|| substr(date,13,2),"+6 hour") * 1000 as date,'+namesensor['name']+
           ' FROM sitetable'+tabla['name']+
        ' ORDER BY date ASC'
    ).fetchall()
    data = []
    for resultado in resultados:
        data.append(list(resultado)) # or simply data.append(list(row))

    return json.dumps(data)

@bp.route('/<int:id>/<int:sensor>/<int:nreg>/datajsonreg')
@login_required
def datajsonreg(id,sensor,nreg):
    db = get_db()

    tabla = db.execute('SELECT name FROM site WHERE id='+str(id)).fetchone()
    namesensor = db.execute('SELECT name FROM sensor WHERE id='+str(sensor)).fetchone()
    #print (namesensor['name'])
    #Falta mandar error cuando no encuentra el sensor
    resultados = db.execute(
        'SELECT * FROM ( SELECT strftime("%s",substr(date,0,5)||"-" ||substr(date,5,2)||"-"||substr(date,7,2)||" "||substr(date,9,2)||":"||substr(date,11,2)||":"|| substr(date,13,2),"+6 hour") * 1000 as date,'+namesensor['name']+
           ' FROM sitetable'+tabla['name']+
        ' ORDER BY date DESC LIMIT '+str(nreg)+') ORDER BY date ASC '
    ).fetchall()
    data = []
    for resultado in resultados:
        data.append(list(resultado)) # or simply data.append(list(row))

    return json.dumps(data)


@bp.route('/<int:id>/<int:sensor>/datajsonlast')
@login_required
def datajsonlast(id,sensor):
    db = get_db()

    tabla = db.execute('SELECT name FROM site WHERE id='+str(id)).fetchone()
    namesensor = db.execute('SELECT name FROM sensor WHERE id='+str(sensor)).fetchone()
    #print (namesensor['name'])
    #Falta mandar error cuando no encuentra el sensor
    resultados = db.execute(
           'SELECT strftime("%s",substr(date,0,5)||"-" ||substr(date,5,2)||"-"||substr(date,7,2)||" "||substr(date,9,2)||":"||substr(date,11,2)||":"|| substr(date,13,2),"+6 hour") * 1000 as date,'+namesensor['name']+
           ' FROM sitetable'+tabla['name']+
        ' ORDER BY date DESC LIMIT 1'
    ).fetchall()
    data = []
    for resultado in resultados:
        data.append(list(resultado)) # or simply data.append(list(row))

    return json.dumps(data)


@bp.route("/graph")
@login_required
def graph():
    templateData = {
        'grafica' : grafica
    }
    return render_template('graph.html',**templateData)
 



