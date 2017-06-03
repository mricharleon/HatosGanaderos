.. HatosGanaderos documentation master file, created by
   sphinx-quickstart on Sun Oct  5 19:31:55 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Instalación
===========

HatosGanaderos es un sistema web que te ayuda con el control y organización de reproducción, alimentación, sanidad y producción de tu entidad ganadera.

Linux
-----

Paso 1:
	(Instalar PIP)

		- sudo apt-get install python-pip python-dev build-essential
		- sudo pip install --upgrade pip

Paso 2:
	(Instalar y configurar virtualenv)

		- sudo pip python-virtualenv
		- virtualenv mi_entorno
		- source mi_entorno/bin/activate

Paso 3:
	(Instalar requerimientos)

		- pip install -r requirements.txt

Paso 4:
	(Instalar Nodejs)

		- sudo apt-get install npm

Paso 5:
	(Instalar ishout.js)

		- npm install ishout.js

Paso 6:
	(Clonar el proyecto de Github)

		-  git clone https://github.com/mricharleon/HatosGanaderos.git

Paso 7:
	(Configurar datos de la base de datos)

		- PFC/SIDGV/settings.py 
	        | 'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        | 'NAME': 'test',
	        | 'USER': 'administrador',
	        | 'PASSWORD': '12345',
	        | 'HOST': '127.0.0.1',
	        | 'PORT': '5432',

Paso 8:
	(Configurar direcciones IP)

		- PFC/SIDGV/settings.py 
			| ISHOUT_CLIENT_ADDR = '192.168.1.2:5500' 
			| SSL_DOMAIN = 'https://192.168.1.2:1290' 

Paso 9:
	(Configurar el correo electrónico)

		- PFC/SIDGV/settings.py
			| EMAIL_HOST = 'smtp.gmail.com'
			| EMAIL_HOST_USER = 'example@gmail.com'
			| EMAIL_HOST_PASSWORD = 'password'
			| EMAIL_PORT = '587'
			| EMAIL_USE_TLS = True

Paso 10:
	(Arranque del sistema)

		- En la terminal dirigirse a: /PFC/SIDGV
			- ./manage.py syncdb
			- gunicorn SIDGV.wsgi:application -w 5

Listo, con estos sencillos pasos ya tendrás instalado y corriendo el proyecto HatosGanaderos.