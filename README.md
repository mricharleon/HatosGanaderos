# HatosGanaderos #
Sistema de Administración y Control de Ganados Vacunos, brinda la posibilidad de gestionar el ganado en cuatro aspectos fundamentales de una entidad ganadera: Reproducción, alimentación, Sanidad y Producción. A través de tecnologías como ** Python, Django, NodeJs, ishout.js, Django Realtime, PostgreSQL, etc. ** 

## Instalación de Hatos Ganaderos ##
Para realizar la instalación se debe preparar un entorno de ejecución:

### Prerrequisitos ###

Instalar PostgreSQL

    sudo apt-get install postgresql-9-4

Cambiar clave a usuario postgres

    sudo passwd postgres

Entrar a la consola de administración de PostgreSQL

    sudo postgres
    psql postgres
    ALTER ROLE postgres PASSWORD 'contraseña_de_usuario';
    \q

Instalar, crear y activar un entorno virtual (virtualenv)

    sudo apt-get install python-virtualenv
    virtualenv -p /usr/bin/python2.7 ~/HatosGanaderos
    source ~/HatosGanaderos/bin/activate

### Instalar ###
	
Clonar el proyecto

Dentro del entorno virtual(~/HatosGanaderos/) activado

    git clone https://github.com/mricharleon/HatosGanaderos.git


## Contacto ##

Para mayor información sobre como probar el sistema, comunicarse a mrleonr@unl.edu.ec
