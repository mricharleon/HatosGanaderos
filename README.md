|docs|

# HatosGanaderos #
Sistema web de Administración y Control de Ganados Vacunos através de **agentes inteligentes deliberativos**, brinda la posibilidad de gestionar el ganado en cuatro aspectos fundamentales de una entidad ganadera: Reproducción, Alimentación, Sanidad y Producción. A través de tecnologías como **Python, Django, NodeJs, ishout.js, Django Realtime, PostgreSQL, SPADE, etc.**

## Documentación
[ReadTheDocs - HatosGanaderos](http://hatosganaderos.readthedocs.io/)

## Instalación con Docker (Recomendada)
Se requiere tener instalado **docker** y **docker-compose** en su equipo

### Clonar proyecto
> Configurar credenciales de CORREO [SIDGV/settings.py]

> Configurar credenciales de OPBEAT para ver datos de **performance** y **errors** en tiempo real. [SIDGV/settings.py]

```shell
$ git clone https://github.com/mricharleon/HatosGanaderos.git
```

### Iniciar docker-compose
> Ingresa en directorio HatosGanaderos

```bash
$ make start
```

### Cargar data inicial
```bash
$ make db
```

### Iniciar spade (Agentes deliberativos)
```bash
$ make spade
```

> **LISTO!** - Ingresa a http://localhost en tu navegador (***user:*** admin, ***pass:*** admin)

### Testeado con:
> Ubuntu 16.04.2 LTS xenial

> Docker version 17.05.0-ce, build 89658be

> docker-compose version 1.13.0, build 1719ceb


------------


## Instalación manual

#### Instalar Python ####
El lenguaje de programación que requiere el sistema es Python en su versión 2.7.

    sudo apt-get install python2.7

#### Instalar PostgreSQL ####
Como motor de BD hace uso de PostgreSQL por ser eficiente.

    sudo apt-get install postgresql-9-4

Cambiar clave a usuario postgres

    sudo passwd postgres

Crear usuario nuevo

    su postgres
    psql
    CREATE USER user_hg PASSWORD 'password';

Asignar permisos a usuario

    ALTER ROLE user_hg WITH SUPERUSER;

Crear BD

    CREATE DATABASE bd_hg WITH OWNER user_hg;
    \q

#### Instalar, crear y activar un entorno virtual (virtualenv) ####

    sudo apt-get install python-virtualenv
    virtualenv -p /usr/bin/python2.7 ~/HatosGanaderos
    source ~/HatosGanaderos/bin/activate

#### Instalar Nodejs ####
Para servir notificaciones en tiempo real se hace necesario utilizar algunas librerías js.

    sudo apt-get install curl
    curl --silent --location https://deb.nodesource.com/setup_0.12 | bash -
    sudo apt-get install --yes nodejs

#### Instalar ishout.js ####
Es una librería necesaria para el envio de notificaciones en tiempo real.

    npm install ishout.js

#### Instalar redis-sever ####

    sudo apt-get install redis-server

#### Instalar Nginx ####
Para servir los datos estáticos del sistema HatosGanaderos se hace uso de nginx.

    sudo apt-get install nginx

Configurar el archivo de configuración de nginx:

    sudo vim /etc/nginx/sites-avalaible/default
    sudo ln -s /etc/nginx/sites-avalaible/default /etc/nginx/sites-enabled/default

En este archivo se coloca la información del archivo que se encuentra dentro de la carpeta conf_nginx

Ahora reiniciamos el servidor

    sudo /etc/init.d/nginx restart

#### Instalar gunicorn ####
Para servir los datos dinámicos del sistema HatosGanaderos se hace uso de gunicorn.

    sudo apt-get install gunicorn

#### Clonar el proyecto ####

Clonar el proyecto dentro del entorno virtual(~/HatosGanaderos/) activado

    git clone https://github.com/mricharleon/HatosGanaderos.git

Instalar librerias con pip

    pip install -r requirements.txt

  > Copiar la carpeta userena en entorno virtual (lib/python2.7/site-packages)

## Ejecución del sistema  ##
Para la ejecución del sistema web HatosGanaderos se requiere seguir los siguientes pasos:

**Importante**
Configurar el settings.py del proyecto como:

> Credenciales de CORREO y OPBEAT(Opcional)

Crear datos por defecto en la BD

    ./manage.py syncdb
    ./manage migrate userena
    ./manage migrate easy_thumbnails
    ./manage migrate django_extensions
    ./manage migrate django_cron
    ./manage migrate guardian

Ahora si con estos pasos a ejecutar el sistema web HatosGanaderos

**Primera Terminal**

    redis-server

**Segunda Terminal**

    node ~/node_modules/ishout.js/server.js

**Tercera terminal**

    configure.py 127.0.0.1
    runspade.py

**Cuarta terminal**

    gunicorn SIDGV.wsgi:application -w4



.. |docs| image:: https://readthedocs.org/projects/hatosganaderos/badge/
    :alt: Documentation Status
    :scale: 100%
    :target: http://hatosganaderos.readthedocs.io/

