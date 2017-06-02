start:
	docker-compose up --build -d

dependencies:
	docker exec app01 /bin/sh -c "pip install -r requirements.txt"

collectstatic:
	docker exec app01 /bin/sh -c "python manage.py collectstatic -i *.styl --noinput"

db:
	docker exec app01 /bin/sh -c "python manage.py syncdb --noinput &&\
		python manage.py migrate userena &&\
		python manage.py migrate easy_thumbnails &&\
		python manage.py migrate django_extensions &&\
		python manage.py migrate django_cron &&\
		python manage.py migrate guardian"
	docker exec app01 /bin/sh -c "python manage.py loaddata fixtures/initial-data.json"

spade:
	docker exec app01 /bin/sh -c "configure.py 127.0.0.1 && runspade.py" &

restart:
	docker-compose down
	docker volume rm hatosganaderos_data-app ; docker-compose up --build
