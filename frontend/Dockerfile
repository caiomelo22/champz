FROM node:16.16.0

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

EXPOSE 8080

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=8080

CMD ["npm", "run", "dev"]