# HatosGanaderos #
Sistema web de Administración y Control de Ganados Vacunos através de **agentes inteligentes deliberativos**, brinda la posibilidad de gestionar el ganado en cuatro aspectos fundamentales de una entidad ganadera: Reproducción, Alimentación, Sanidad y Producción. A través de tecnologías como **Python, Django, NodeJs, ishout.js, Django Realtime, PostgreSQL, SPADE, etc.** 

## Instalación de Hatos Ganaderos ##
Para realizar la instalación se debe preparar un entorno de ejecución:

#### Instalar Python ####
El lenguaje de programación que requiere el sistema es Python en su versión 2.7.

    sudo apt-get install python2.7

#### Instalar PostgreSQL ####
Como motor de BD hace uso de PostgreSQL por ser eficiente.

    sudo apt-get install postgresql-9-4

Cambiar clave a usuario postgres

    sudo passwd postgres

Crear usuario nuevo

    sudo postgres
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

## Ejecución del sistema  ##
Para la ejecución del sistema web HatosGanaderos se requiere seguir los siguientes pasos:

**Importante**
Configurar el settings.py del proyecto como:

 * La dirección ip de tu máquina(en el archivo se especifica donde modifiques)

Crear datos por defecto en la BD

    ./manage.py syncdb

Ahora si con estos pasos a ejecutar el sistema web HatosGanaderos

**Primera Terminal**

    redis-server

**Segunda Terminal**

    node ~/node_modules/ishout.js/server.js

**Tercera terminal**

    configure.py 127.0.0.1
    runspade.py

**Cuarta terminal**

    gunicorn ~/HatosGanaderos/HatosGanaderos/SIDGV.wsgi:application -w3



## Contacto ##

Para mayor información sobre como probar el sistema, comunicarse a mrleonr@unl.edu.ec
