# HatosGanaderos #
Sistema web de Administración y Control de Ganados Vacunos através de **agentes inteligentes deliberativos**, brinda la posibilidad de gestionar el ganado en cuatro aspectos fundamentales de una entidad ganadera: Reproducción, Alimentación, Sanidad y Producción. A través de tecnologías como **Python, Django, NodeJs, ishout.js, Django Realtime, PostgreSQL, SPADE, etc.** 

## Instalación de Hatos Ganaderos ##
Para realizar la instalación se debe preparar un entorno de ejecución:

### Prerrequisitos ###

#### Instalar Python ####
El lenguaje de programación que requiere el sistema es Python en su versión 2.7.

    sudo apt-get install python2.7

#### Instalar PostgreSQL ####
Como motor de BD hace uso de PostgreSQL por ser eficiente.

    sudo apt-get install postgresql-9-4

Cambiar clave a usuario postgres

    sudo passwd postgres

Entrar a la consola de administración de PostgreSQL

    sudo postgres
    psql postgres
    ALTER ROLE postgres PASSWORD 'contraseña_de_usuario';
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

#### Instalar Nginx ####
Para servir los datos estáticos del sistema HatosGanaderos se hace uso de nginx.

#### Instalar gunicorn ####
Para servir los datos dinámicos del sistema HatosGanaderos se hace uso de gunicorn.

### Instalar HatosGanaderos ###
	
Clonar el proyecto dentro del entorno virtual(~/HatosGanaderos/) activado

    git clone https://github.com/mricharleon/HatosGanaderos.git

Instalar librerias con pip

    pip install -r requirements.txt

## Ejecución del sistema  ##
Para la ejecución del sistema web HatosGanaderos se requiere seguir los siguientes pasos:



## Contacto ##

Para mayor información sobre como probar el sistema, comunicarse a mrleonr@unl.edu.ec
