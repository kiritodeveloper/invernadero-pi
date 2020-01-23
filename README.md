Este es un proyecto que utiliza python flask, sqlite3, I32CTT y highcharts para poder visualizar y configurar sensores en arduinos.

Esta version se a utilizado el ejemplo que aparece en este blog https://www.fontenay-ronan.fr/dynamic-charts-with-highcharts-sqlite-and-python/

## Instrucciones ejecutarlo en  debian

```
 apt install python3 python3-flask python3-flask-flatpages sqlite3 git
 git clone https://github.com/neozerosv/invernadero-pi
 cd invernadero-pi
 # Si se quiere usar la version en desarrollo ejecutar 
 git checkout develop
 source .initflask 
 flask init-db
 flask run
```
Para ejecutarlo en un ambiente virtual y que se pueda ver en la red local
```
 apt install python3 python-sqlite sqlite3 git python3-venv
 git clone https://github.com/neozerosv/invernadero-pi
 cd invernadero-pi
 # Si se quiere usar la version en desarrollo ejecutar
 git checkout develop
 python3 -m venv venv/
 source venv/bin/activate
 pip3 install flask
 pip3 install apscheduler
 source .initflask
 flask init-db
 flask run --host=0.0.0.0
```
Se se va ejecutar en una raspberry PI con modulo 802.15.4-radio deberán instalar los siguientes módulos de python antes de inicializar la base:
 pip3 install apscheduler
 pip3 install rpi.gpio
 pip3 install spidev

Luego deberán abrir la direccion http://127.0.0.1:5000/auth/login el usuario y clave por defecto son: admin:admin


El sistema deberá tener:
- [X] Administración de usuarios y grupos
- [X] Administración de lugares (invernaderos) 
- [X] Administración sensores en cada invernadero
- [ ] Administración de actuadores determinando sus valores de configuracion
- [ ] Agregar de alertas via email u otras cosas
- [X] Graficas de los valores historicos de los sensores
- [X] Graficas de los sensores actuales de cada lugar (invernadero)
- [ ] Modificar el dashboard para agregar sensores seleccionados por el usuario
- [ ] Integracion con las lecturas de los lugares
- [ ] Gestion de logs para los eventos de lecturas de sensores y eventos



![Captura de grafica](https://github.com/neozerosv/invernadero-pi/raw/develop/images/invernadero-pi-grafica-bruto.png)

## ToDo
- [ ] Mejorar el menu de navegacion
- [X] Agrupar los sensores por lugares
- [ ] Actualizar las gráficas dinamicamente
- [ ] Verificar la devolucion de valores nulos
- [ ] Agregar un modulo de traduccion de interfaz
- [ ] Cambiar la programación usando clases
- [ ] Hacer widgets de arrastrar para graficas de sensonres


