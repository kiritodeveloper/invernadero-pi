import functools
import datetime
import time
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
datatypes = ["integer","real","datetime"]

@bp.route('/index')
def index():
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
    return render_template('dashboard/index.html', sensores=sensores,lugares=lugares)

@bp.route('/<int:id>/<int:sensor>/datajson')
def datajson(id,sensor):
    db = get_db()


    tabla = db.execute('SELECT name FROM site WHERE id='+str(id)).fetchone()
    namesensor = db.execute('SELECT name FROM sensor WHERE id='+str(sensor)).fetchone()
    print (namesensor['name'])
    #Falta mandar error cuando no encuentra el sensor
    resultados = db.execute(
            'SELECT date,'+namesensor['name']+
            ' FROM sitetable'+tabla['name']+
        ' ORDER BY date ASC'
    ).fetchall()

    #Para convertir la fecha en formato %Y%m%d%H%M%S a fechaHora POSIX 
    #de la lista de tuplas para que se pueda graficar correctamente
    for i1,fila in enumerate(resultados):
        for i2,dato in enumerate(fila):
            #print (i1,i2,fila,dato,resultados [i1][i2])
            if i2 == 0:
                temp=list(fila)
                fecha=datetime.datetime.strptime(str(resultados[i1][i2]),'%Y%m%d%H%M%S') 
                temp[0]=time.mktime(fecha.timetuple())*1000
                resultados[i1]=tuple(temp)
    #print (results)
    return json.dumps(resultados)



@bp.route("/graph")
def graph():
    templateData = {
        'grafica' : grafica
    }
    return render_template('graph.html',**templateData)
 



