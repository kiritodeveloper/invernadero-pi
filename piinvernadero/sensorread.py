#!/usr/bin/python1
import RPi.GPIO as gpio
from .lib.i32cttpy.phy.at86rf233_rpi.driver import driver_at86rf233
from .lib.i32cttpy.mac.ieee802154.driver import driver_ieee802154
from .lib.i32cttpy.i32ctt.driver import driver_i32ctt
from time import sleep


""" Demonstrating Flask, using APScheduler. """

import time
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def read_sensors():
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
        pares = i32ctt.leer_registros(0x0201, 1, [2, 3])
        #Se imprime la lista de tuplas retornada por el otro nodo (poseen la misma estructura que se le
        #pasa a la funcion de escritura)
        if pares:
            for i in pares:
                print("Registro {}: 0x{:08X}".format(i[0], i[1]))
                print("-", i[1])
        else:
            print("No hubo respuesta al leer")

    finally:
        gpio.cleanup()

