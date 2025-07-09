# Build phase
FROM node:18 AS builder

WORKDIR /app

COPY /package*.json ./
RUN npm install
RUN npm install
RUN npm install --save-dev @types/leaflet


COPY . ./
RUN npm run build

# Serve phase using nginx
FROM nginx:stable-alpine

# Copy build files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config (optional)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
