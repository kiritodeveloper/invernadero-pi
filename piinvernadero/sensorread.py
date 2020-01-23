#!/usr/bin/python1
import RPi.GPIO as gpio
from .lib.i32cttpy.phy.at86rf233_rpi.driver import driver_at86rf233
from .lib.i32cttpy.mac.ieee802154.driver import driver_ieee802154
from .lib.i32cttpy.i32ctt.driver import driver_i32ctt
from time import sleep


""" Demonstrating Flask, using APScheduler. """

import sqlite3
import time
import os
import array
print(os.path.abspath('.')+'/instance/invernadero.sqlite')

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def read_sensors():
    conn = sqlite3.connect(os.path.abspath('.')+'/instance/invernadero.sqlite')
    conn.row_factory = sqlite3.Row #Para que use indices de nombres de columnas


    #En caso de usar un radio con PA/LNA, cuya direccion de comunicacion es controlada por el AT86RF233
    #y cuyo control de pass through se controla por GPIO, se puede usar esta linea:
    #phy = driver_at86rf233(gpio, FEM_TXRX = True, pin_FEM_CPS = 15)

    #Para radios de OpenLabs (Raspberry Pi 802.15.4 radio) se usa esta linea:
    phy = driver_at86rf233(gpio)

    #Se instancia el driver de MAC, pasandole el driver de PHY
    mac = driver_ieee802154(phy)

    #Se instancia el driver de I32CTT, pasandole el driver de MAC
    i32ctt = driver_i32ctt(mac)

    #Configura el radio 802.15.4
    mac.escr_config_red(canal=26, pan_id=0xCAFE, dir_corta=0x0100)

    try:
        for row in conn.execute('SELECT * FROM site WHERE enabled=1 ORDER BY id'):

            #Generando el SQL y los valores de la conexion via I32CCT
            sensores=" "
            valores=" "
            siteid=row['id']
            sitename=row['name']
            siteaddress=row['address']

            c = conn.cursor()
            c.execute('SELECT name FROM sensor WHERE  site_id = '+str(siteid))
            rows=c.fetchall()
            nsensores=len(rows)
            if nsensores>0:
                #Obteniendo el numero de  direcciones a leer del arduino            
                paresaddress = list(range(nsensores*2))

                #Construyendo la sentencia SQL para leer los sensores en la tabla del sitio
                for sensor in rows:
                    sensores=sensores+" ,"+sensor['name']
                    valores=",?"+valores
                sql='INSERT INTO sitetable'+sitename+"(date"+sensores+") VALUES (?"+valores+")"

                #Lee las direcciones 0,1  (temperatura) y 2,3 (humedad) (Ver el codigo de python
                #pares = i32ctt.leer_registros(0x0201, 1, [0, 1, 2, 3])
                pares = i32ctt.leer_registros(int("0x0"+str(siteaddress),16), 1, paresaddress)
                #Se imprime la lista de tuplas retornada por el otro nodo (poseen la misma estructura que se le
                #pasa a la funcion de escritura)

                if pares:
                    valores=(time.strftime("%Y%m%d%H%M%S"),)
                    for elemento in range(nsensores):
                        #Genera la tupla con (date, sensor1, sensor2, sensorN)
                        temp=valores
                        valores=temp+(pares[(2*elemento)][1]+(pares[2*elemento+1][1]/100),)
                    lectura = [valores]
                    #lectura = [(time.strftime("%Y%m%d%H%M%S"), pares[0][1]+(pares[1][1]/100), pares[2][1]+(pares[3][1]/100) )]
                    print(lectura)
                    #conn.executemany('INSERT INTO sitetableinvernadero1(date,cTemp,humidity)  VALUES (?,?,?)', lectura)
                    print("conn.executemany("+sql+","+ str(lectura)+")")
                    conn.executemany(sql, lectura)
                    conn.commit()
                else:
                    print("No hubo respuesta al leer los sensores del sitio "+sitename+" con direccion "+str(siteaddress) )
            else:
                print("No existen sensores registrados en la base de datos para el sitio "+sitename+" con direccion "+str(siteaddress) )

    finally:
        gpio.cleanup()
        conn.close()

