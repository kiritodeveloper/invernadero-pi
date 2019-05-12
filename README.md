<<<<<<< HEAD

Este es un proyecto que utiliza python flask, sqlite3 y highcharts para poder visualizar y configurar sensores en arduinos.

## Instrucciones ejecutarlo en  debian

```
 apt install python3-flask python3-flask-flatpages sqlite3 git
 git clone https://github.com/neozerosv/invernadero-pi
 cd invernadero-pi
 # Si se quiere usar la version en desarrollo ejecutar 
 git checkout develop
 . .initflask 
 flask init-db
 flask run
```
El sistema deberá tener:
- [X] Administración de usuarios y grupos
- [X] Administración de lugares (invernaderos) 
- [X] Administración sensores en cada invernadero
- [ ] Administración de actuadores determinando sus valores de configuracion
- [ ] Agregar de alertas via email u otras cosas
- [X] Graficas de los valores historicos de los sensores
- [X] Graficas de los sensores actuales de cada lugar (invernadero)
- [ ] Modificar el dashboard para agregar sensores seleccionados por el usuario
- [ ] Integracion con las lecturas de los luagares

El usuario y clave por defecto son: admin:admin


![Captura de grafica](https://github.com/neozerosv/invernadero-pi/raw/develop/images/invernadero-pi-grafica-bruto.png)

## ToDo
- [ ] Mejorar el menu de navegacion
- [X] Agrupar los sensores por lugares
- [ ] Actualizar las gráficas dinamicamente
- [ ] Verificar la devolucion de valores nulos
- [ ] Agregar un modulo de traduccion de interfaz
- [ ] Hacer widgets de arrastrar para graficas de sensonres
=======
# invernadero-pi
Sistema para la configuracion y monitoreo de sensores en la raspberry pi con python, flask, highcharts

Esta version se a utilizado el ejemplo que aparece en este blog https://www.fontenay-ronan.fr/dynamic-charts-with-highcharts-sqlite-and-python/
>>>>>>> c8ca33abe683c96ae64ae1a7575f7ebb5a7ac19d
