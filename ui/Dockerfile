# UI Dockerfile
FROM node:20-bullseye
WORKDIR /app

# Clean up any previous lock or modules
RUN rm -rf node_modules package-lock.json || true

COPY package.json ./
# Only copy package-lock.json if it exists
RUN if [ -f package-lock.json ]; then cp package-lock.json ./; else npm install --package-lock-only; fi
RUN npm install
RUN npm rebuild

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
