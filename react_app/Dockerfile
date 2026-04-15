FROM node:20-alpine

WORKDIR /app

# Copy package.json and vite configs
COPY package*.json ./
COPY vite.config.js ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server on host 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
