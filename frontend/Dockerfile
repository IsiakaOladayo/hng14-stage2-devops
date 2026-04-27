# Stage 1
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Stage 2
FROM node:18-alpine
WORKDIR /app

RUN adduser -D appuser

COPY --from=builder /app .

USER appuser

EXPOSE 3000

HEALTHCHECK CMD wget --spider http://localhost:3000 || exit 1

CMD ["node", "app.js"]
