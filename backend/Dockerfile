# Stage 1: Build the webapp
FROM node:22 AS webapp-build
WORKDIR /webapp/rgb_app

# Suppress npm update notices during build
ENV NPM_CONFIG_UPDATE_NOTIFIER=false

# Copy package files first for better Docker layer caching
COPY webapp/rgb_app/package*.json ./

# Install all dependencies (including devDependencies needed for build)
# Then fix any security vulnerabilities with compatible updates
RUN npm install --include=dev && npm audit fix || true

# Copy source files (node_modules excluded via .dockerignore)
COPY webapp/rgb_app/ ./

# Build the app
RUN npm run build

# Stage 2: Build the backend
FROM python:3.10-slim AS backend
WORKDIR /app

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Install backend dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY *.py ./

# Copy built webapp static files
COPY --from=webapp-build /webapp/rgb_app/dist ./static

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start backend (serves API, WebSocket, and static files)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]