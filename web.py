#!/usr/bin/python3
from flask import Flask, render_template, request
import sqlite3
import datetime
import time
import pytz
import json

app = Flask(__name__)
 
grafica = "Invernadero 1"
base = "invernaderoprueba.db"
 
@app.route("/data.json")
def data():
    connection = sqlite3.connect(base)
    cursor = connection.cursor()
    cursor.execute("SELECT date, Ctemp from invernadero1")
    results = cursor.fetchall()
    print (type(results))
    print (type(results[0]))
    #Para convertir la fecha en formato %Y%m%d%H%M%S a fechaHora POSIX 
    #de la lista de tuplas para que se pueda graficar correctamente
    for i1,fila in enumerate(results):
        for i2,dato in enumerate(fila):
            print (i1,i2,fila,dato,results [i1][i2])
            if i2 == 0:
                temp=list(fila)
                fecha=datetime.datetime.strptime(results[i1][i2],'%Y%m%d%H%M%S') 
                temp[0]=time.mktime(fecha.timetuple())*1000
                results[i1]=tuple(temp)
    #print (results)
    return json.dumps(results)

@app.route("/graph")
def graph():
    templateData = {
        'grafica' : grafica
    }
    return render_template('graph.html',**templateData)
 
 
if __name__ == '__main__':
    app.run(
    debug=True,
    threaded=True,
    host='0.0.0.0'
)
