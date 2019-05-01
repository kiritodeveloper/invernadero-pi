
Este es un proyecto para que utiliza python flask, sqlite3 y highcharts para poder visualizar y configurar sensores en arduinos.

## Instrucciones ejecutarlo en  debian

```
 apt install python3-flask python3-flask-flatpages sqlite3 git
 git clone https://github.com/neozerosv/invernadero-pi
 . .initflask
 flask init-db
 flask run
```

El usuario y clave por defecto son: admin:admin
Captura de pantalla
![alt text](https://raw.githubusercontent.com/neozerosv/invernadero-pi/tree/develop/images/invernadero-pi-grafica-bruto.png)

## ToDo
- [ ] Mejorar el menu de navegacion
- [ ] Agrupar los sensores por lugares
- [ ] Veriicar la devolucion de valores nulos
- [ ] Agregar un modulo de traduccion de interfaz
- [ ] Hacer widgets de arrastrar para graficas de sensonres
