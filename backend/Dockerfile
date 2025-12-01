# Stage 1: Build the webapp
FROM node:18 AS webapp-build
WORKDIR /webapp/rgb_app

# Copy package files first for better Docker layer caching
COPY webapp/rgb_app/package*.json ./

# Install all dependencies (including devDependencies needed for build)
RUN npm install --include=dev

# Copy source files (node_modules excluded via .dockerignore)
COPY webapp/rgb_app/ ./

# Build the app
RUN npm run build

# Stage 2: Build the backend
FROM python:3.10-slim AS backend
WORKDIR /app

# Install backend dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY *.py ./

# Copy built webapp static files
COPY --from=webapp-build /webapp/rgb_app/dist ./static

# Expose port
EXPOSE 8000

# Start backend (serves API, WebSocket, and static files)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]