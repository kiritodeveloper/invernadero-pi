
Este es un proyecto para que utiliza python flask, sqlite3 y highcharts para poder visualizar y configurar sensores en arduinos.

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
- [ ] Graficas de los sensores actuales de cada lugar (invernadero)


El usuario y clave por defecto son: admin:admin


![Captura de grafica](https://github.com/neozerosv/invernadero-pi/raw/develop/images/invernadero-pi-grafica-bruto.png)

## ToDo
- [ ] Mejorar el menu de navegacion
- [ ] Agrupar los sensores por lugares
- [ ] Actualizar las gráficas dinamicamente
- [ ] Veriicar la devolucion de valores nulos
- [ ] Agregar un modulo de traduccion de interfaz
- [ ] Hacer widgets de arrastrar para graficas de sensonres
