FROM python:2.7.12

WORKDIR /usr/src/app

ENV DB_NAME=bd_hg
ENV DB_USER=user_hg
ENV DB_PASS=12345
ENV DB_SERVICE=db
ENV DB_PORT=5432

# Necesario para generar documentación en formato LatexPDF
#RUN apt-get install texlive-formats-extra && \
#apt-get install latexmk
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-subj "/C=''/ST=''/L=''/O=''/CN=''" -keyout nginx.key -out nginx.crt

ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD userena /usr/src/app
RUN rm -rf /usr/lib/python2.7/dist-packages/userena
COPY userena /usr/local/lib/python2.7/site-packages/userena
ADD . /usr/src/app/
RUN ./manage.py collectstatic -i *.styl --noinput
