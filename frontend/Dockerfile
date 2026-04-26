FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN adduser -D appuser
USER appuser

EXPOSE 3000

HEALTHCHECK CMD wget --spider http://localhost:3000/health || exit 1

CMD ["npm", "start"]
