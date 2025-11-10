# Stage 1: Build the webapp
FROM node:18 AS webapp-build
WORKDIR /webapp
COPY webapp/rgb_app/ ./rgb_app/
WORKDIR /webapp/rgb_app
RUN npm install && npm run build

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