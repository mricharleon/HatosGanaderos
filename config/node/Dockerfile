FROM node:6.0.0

RUN mkdir /src
WORKDIR /src
RUN npm install ishout.js
COPY . /src
CMD ["node", "node_modules/ishout.js/server.js", "--config=ishout.config.json"]
