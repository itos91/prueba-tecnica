# Prueba tecnica Tarea1 : Aplicación Python para lectura de datos de un sensor

## Requisitos

Este proyecto está implementado en Python versión 3.12.

Para ello, es recomendable usar un entorno virtual e instalar los los paquetes que que están en requirements.txt mediante el siguiente comando.

`pip install -r requirements.txt`

Para poder ejecutar este proyecto, es necesario tener un servidor nats para mensajería y un servidor MySQL para bases de datos.

### Servidor NATS

Para crear un servidor NATS, yo recomiendo tener instalado Dockers y ejecutar los siguientes comandos para crear un contenedor:

```bash
docker pull nats
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name nats-server -d -ti nats:latest
```

### Servidor MySQL

Para crear un servidor MySQL, yo recomiendo tener instalado Dockers y ejecutar los siguientes comandos para crear un contenedor:

```bash
docker pull mysql
docker run  --name sql-server -e MYSQL_ROOT_PASSWORD=password -p 3307:3306 -v sql-data:/var/lib/mysql -d mysql
```

donde MYSQL_ROOT_PASSWORD le ponemos la contraseña que queramos.

Una vez creado el contenedor, y lo tenemos iniciado, nos metemos dentro y ejecutamos los siguientes comandos:

```bash
mysql -u root -p
CREATE DATABASE sensor_data;
CREATE TABLE IF NOT EXISTS sensor_data (timestamp TEXT, data TEXT);
```

## Estructura del Proyecto

- **sensor_app/**: Código fuente principal de la aplicación.
- **tests/**: Pruebas unitarias para la aplicación.
- **examples/**: Scripts de ayuda para el proyecto.
- **.gitignore**: Archivos y directorios que Git debe ignorar.
- **README.md**: Información general del proyecto.
- **requirements.txt**: Dependencias del proyecto.

## Cómo Ejecutar

```bash
pip install -r requirements.txt
python -m sensor_app.main --sensor mockup --freq 5 --min_value 0 --max_value 65535 --db_uri mysql://root:password@localhost:3307/sensor_data
```

Donde pasamos los siguientes parámetros:

- **--sensor**: Tipo de sensor. Puede ser mockup o real.
- **--freq**: Frecuencia de lectura del sensor (en segundos).
- **--min_value**: Valor mínimo para generar el sensor infrarrojo cuando es de tipo mockup.
- **--max_value**: Valor máximo para generar el sensor infrarrojo cuando es de tipo mockup.
- **--db_uri**: URI de conexión con la base de datos MySQL.

# Entorno de desarrollo

El entorno de desarrollo integrado (IDE) usado es Visual Code Studio. Para poder ejecutar los script y su debug se usó el siguiente archivo launch.json:

```python
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Publish start sensor message",
            "type": "debugpy",
            "request": "launch",
            "program": "examples/nats_publish.py",
            "console": "integratedTerminal",
            "args": [
                "--subject", "sensor.start",
                "--message", "start"
            ]
        },
        {
            "name": "Publish stop sensor message",
            "type": "debugpy",
            "request": "launch",
            "program": "example/nats_publish.py",
            "console": "integratedTerminal",
            "args": [
                "--subject", "sensor.stop",
                "--message", "stop"
            ]
        },
        {
            "name": "Nats handler",
            "type": "debugpy",
            "request": "launch",
            "program": "src/sensor_app/main.py",
            "console": "integratedTerminal",
            "args": [
                "--min_value", "0",
                "--max_value", "65536",
                "--sensor", "mockup",
                "--freq", "5",
                "--db_uri", "mysql://root:sqlserver@localhost:3307/sensor_data"
            ]
        },
        {
            "name": "Subscribe messages",
            "type": "debugpy",
            "request": "launch",
            "program": "examples/nats_subscribe.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Insert data",
            "type": "debugpy",
            "request": "launch",
            "program": "examples/db_insertData.py",
            "console": "integratedTerminal",
            "args": [
                "--db_uri", "mysql://root:sqlserver@localhost:3307/sensor_data"
            ]
        }
    ]
}
```