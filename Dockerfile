# Dockerfile

# Stage 1: Build React frontend
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Build Python backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend code and built assets
COPY --from=frontend-build /app/frontend /app/frontend

# Create startup script to run both services
RUN echo '#!/bin/bash \n\
    cd /app/backend \n\
    python app.py --port 5000 & \n\
    cd /app/frontend \n\
    npx serve -s build -l 3000' > /app/start.sh && \
    chmod +x /app/start.sh

# Install serve for frontend static serving
RUN npm install -g serve

# Expose ports
EXPOSE 3000 5000

# Start both services
CMD ["/app/start.sh"]