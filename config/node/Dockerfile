FROM node:6.0.0

RUN mkdir /src
WORKDIR /src
RUN npm install ishout.js
COPY . /src
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-subj "/C=''/ST=''/L=''/O=''/CN=''" -keyout key.key -out crt.crt
CMD ["node", "node_modules/ishout.js/server.js", "--config=ishout.config.json"]
