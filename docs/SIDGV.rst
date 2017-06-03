SIDGV package
=============

Introducción
------------

El propósito de este manual del programador es dar a conocer al lector todos las secciones de código que se han utilizado en la construcción del sistema HatosGanaderos.

HatosGanaderos hace uso del framework Django el cuál contiene algunos archivos de configuración principales ya sea para el correcto funcionamiento del sistema o para colocarlo en producción a HatosGanaderos. Cuenta con algunos puntos que son:
    
    - Archivo de configuración
    - Rooteo de direcciones
    - Wsgi (Producción del sistema)


SIDGV.settings module
---------------------

El archivo de configuración de HatosGanaderos está destinado a manejar la parte base del sistema web, para ello se cuenta con partes importantes en el archivo **settings.py** tales como:

Definir versión de trabajo:
    (Desarrollo o Producción)
    
    Django a través de una fácil configuración permite tener el sistema ya sea en desarrollo o en producción. 

        - **La variable DEBUG** si está en *False* inidica que esta en produción y si esta en *True* indica que está en desarrollo.
        - **Si está en producción** es necesario hacer uso de la variable *ALLOWED_HOSTS* que sera la encargada de almacenar la o las ip que serán el dominio del sistema HatosGanaderos.

.. py:function:: Código

    | DEBUG = False
    | TEMPLATE_DEBUG = DEBUG
    | ALLOWED_HOSTS = ['DIRECCIÓN IP DEL DOMINIO']


Base de datos:
    (Parámetros de configuración)
    
    Para realizar la configuración de la base de datos que vamos a usar para establecer la concexión a ella es muy fácil y se lo realiza de la siguiente manera:

        - **ENGINE** indica el motor de base de datos a usar.
        - **NAME** nombre de la base de datos.
        - **USER** usuario administrador de la base de datos.
        - **PASSWORD** clave del usuario con acceso a la base de datos.
        - **HOST** la ip con la que se va a concetar al sistema.        
        - **PORT** puerto que utiliza la base de datos.
        

.. py:function:: Código:

    DATABASES = {
        'default': {
            | 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            | 'NAME': 'bdHatosGanaderos',
            | 'USER': 'administrador',
            | 'PASSWORD': 'securepassword',
            | 'HOST': '127.0.0.1',
            | 'PORT': '5432',
        }
    }


Internalización:
    (Parámetros de idiomas y zonas horarias)
    
    La internalización se puede configurar en esta variable así mismo la zona horaria, que son necesarias para poder obtener un buen manejo de tiempos en el sistemas.

.. py:function:: Código:

    | TIME_ZONE = 'America/Guayaquil'
    | LANGUAGE_CODE = 'es-EC'
    | LANGUAGES = ( ('es', ugettext('Spanish')), )
    | LOCALE_PATHS = ( os.path.join(PROJECT_ROOT, 'locale'), )
    | USE_I18N = True
    | USE_L10N = True
    | USE_TZ = True


Media y Static:
    (Administrar archivos de contenido)
    
    Para que el sistema pueda alvergar la información dígase: imagenes, css, js. Dentro del sistema que esta denominado internamente HatosGanderos (SIDGV, Sistema Inteligente Deliberativo de Ganado Vacuno).

.. py:function:: Código:

    | MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public/media/')
    | MEDIA_URL = '/media/'
    | STATIC_ROOT = os.sep.join(os.path.abspath( __file__).split( os.sep)[:-2] + ['static'])
    | STATIC_URL = '/static/'
    | STATICFILES_DIRS = ( os.path.join(PROJECT_ROOT, 'SIDGV/static/'), )

Userena:
    (Gestión de usuarios)
    
    Para poder tener en el sistema un control mejorado de los usuarios se utilizo la libreria denominada userena con las debidas adaptaciones a los requerimientos, como parámetros iniciales se cuenta con el siguiente.

        - **LOGIN_REDIRECT_URL** ruta luego de realizar el login correctamente.
        - **LOGIN_URL** ruta para realizar el login.
        - **LOGOUT_URL** ruta para realizar el logout.
        - **AUTH_PROFILE_MODULE** se conceta con la app de profiles para retomar datos.
        - **USERENA_DISABLE_PROFILE_LIST** listado de usuarios.
        - **USERENA_MUGSHOT_SIZE** tamaño en pixels para el mugshot de los usuarios.


.. py:function:: Código:

    | LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
    | LOGIN_URL = '/accounts/signin/'
    | LOGOUT_URL = '/accounts/signout/'
    | AUTH_PROFILE_MODULE = 'profiles.Profile'
    | USERENA_DISABLE_PROFILE_LIST = True
    | USERENA_MUGSHOT_SIZE = 140


Django RealTime:
    (Librería que permite el envío de mensajes en tiempo real)
    
    En el sistema se utiliza el envío de mensajes en tiempo real ya sea para el módulo de notificaciones como el de mensajería, y se hizo uso de varias librerias entre ellas están: 

        - DjangoRealTime
        - ishout.js
        - socket.io
        - redis

    Que son las que se requieren para crear un socket para cada comunicación através de una conexión segura. 

        - **ISHOUT_CLIENT_ADDR** la ip del dominio del sistema.
        - **ISHOUT_API_ADDR** ip de la librería ishout.
        - **ISHOUT_HTTPS** utiliza https.

    .. note::
        Cabe recalcar que estas deben ir incluidas en la tupla INSTALLED_APPS que se encuentra en el archivo **settings.py**

.. py:function:: Código:

    | ISHOUT_CLIENT_ADDR = 'DIRECCIÓN IP DE HATOS GANADEROS' 
    | ISHOUT_API_ADDR = '127.0.0.1:6600'
    | ISHOUT_HTTPS = True


Correo Electrónico:
    (Configurar el correo electrónico)
    
    El sistema cuando crea cuentas y resetea claves envia un email al correo registrado esto para poder validar la autenticidad del usuario, para poder obtener aquella funcionalidad se configura las siguientes variables:

        - **EMAIL_HOST** utilizamos smtp para poder utilizar gmail.
        - **EMAIL_HOST_USER** se especifica el email que va ser usado por el sistema.
        - **EMAIL_HOST_PASSWORD** la clave de dicha cuenta de correo.
        - **EMAIL_PORT** puerto por el cuál se envían los correos.
        - **EMAIL_USE_TLS** usar conexión segura.


.. py:function:: Código:

    | EMAIL_HOST = 'smtp.gmail.com'
    | EMAIL_HOST_USER = ''
    | EMAIL_HOST_PASSWORD = ''
    | EMAIL_PORT = '587'
    | EMAIL_USE_TLS = True

Script para redireccionar con https:
    (Establecer el 'https' delante de las urls)
    
    El sistema ya esta configurado para trabajar con https en el servidor **Nginx** pero en **Django** es necesario hacer algo más para obtener mejor funcionalidad. Para ello se escribe un decorador en el archivo **__init__.py**.

    .. py:function:: __init__.py: 
        
        from django.core import urlresolvers
        
        from django.conf import settings
        
        def reverse_decorator(func):
            def inner(*args, **kwargs):
                
                abs_path = func(*args,**kwargs)
                
                if settings.SSL_DOMAIN and settings.SSL_SECTIONS and settings.SSL_DOMAIN.startswith('https'):
                    for section in settings.SSL_SECTIONS:
                        if abs_path.startswith(section):
                            abs_path = settings.SSL_DOMAIN + abs_path
                            break
                return abs_path        
            return inner
        urlresolvers.reverse = reverse_decorator(urlresolvers.reverse)
    

    Lo que hace es tomar la direcciones que esten la tupla del **settings.py** y anteponerles el https y redireccionar correctamente.

    En el **settings** deberá ir de la siguiente manera.


    .. py:function:: Código:
    
        | USE_TLS = True
        | SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
        | SSL_DOMAIN = 'https://DIRECCIÓN IP DE HATOS GANADEROS'
        | SSL_SECTIONS = (
            '/list_cattle',
            '/agrega_ganaderia_config',
            '/agrega_ganado_ordenio',
            '/list_cattle_male',
            '/lista_ganado_produccion',
            '/list_insemination',
            '/list_food',
            '/list_wormer',
            '/list_vaccine',
            '/accounts',
            '/add_attempt_service',
            '/admin',
            '/messages',
        )






SIDGV.urls module
-----------------

El archivo de Url's contiene el rooteo de direcciones solicitadas por el cliente, para luego enviar al archivo **views.py** donde se encontrará la lógica y luego retornará una página html con datos y la enviará como resultado al cliente.

.. py:function:: Código:

    | from django.conf.urls import patterns, url, include
    | from django.conf import settings
    | from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    | from django.conf.urls.static import static
    | from django.contrib import admin
    | admin.autodiscover()
    | import django_cron
    | #django_cron.autodiscover()
    | urlpatterns = patterns('',
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        (r'^admin/', include(admin.site.urls)),
        ...
        ...
    | )
    | urlpatterns += staticfiles_urlpatterns()
    | urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



Server
------

Se utiliza el servidor nginx para brindar mayor rendimiento por parte del servidor al cliente ya que presta gran cantidad de ventajas, en el sistema HatosGanaderos es utilizado para servir los archivos estáticos del sistema y en la parte dinámica se encuentra gunicorn.

Se necesita configurar algunos parámetros como:
    
    - Dirección ip y puerto en el que escucha.
    - Dirección del proxy interno (127.0.0.1:8000).
    - Certificado de seguridad (SSl).
    - Rutas para los archivos estáticos.

dichas configuraciones se deberán realizar dentro del archivo que se encuentra en **/etc/nginx/sites-enabled/default** como se indica a continuación.

.. py:function:: Código:

    | server {
        
        | listen 80 default_server;
        | listen [DIRECCION IP DEL DOMINIO]:80 default_server ipv6only=on;
        | server_name 127.0.0.1;
        | listen 443 ssl;
        | ssl on;
        | root /usr/share/nginx/html;
        | index index.html index.htm;
        | error_page 497 https://$host:$server_port$request_uri;
        | ssl_certificate             /etc/nginx/ssl/nginx.crt;
        | ssl_certificate_key         /etc/nginx/ssl/nginx.key;
        | ssl_protocols               SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        | ssl_ciphers                 HIGH:!aNULL:!MD5:!3DES;
        | ssl_prefer_server_ciphers   on;
        | location /static/ {
            
            | alias /RUTA DEL PROYECTO/static/;
            | expires 30d;
        | }
        | location /media/ {
            
            | alias /RUTA DEL PROYECTO/public/media/;
            | expires 30d;
        | }   
        | location / {
            
            | proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                
                | proxy_set_header Host $http_host;
                | proxy_redirect off;
                | proxy_pass http://127.0.0.1:8000;
                | proxy_pass_header Server;
                | proxy_set_header X-Real-IP $remote_addr;
                | proxy_connect_timeout 10;
                | proxy_read_timeout 10;
        }
    }


