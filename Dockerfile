# IncuBrix AEO / SEO / GEO Visibility Engine — Production Dockerfile
# Combines Node.js 22 LTS (Express + Vite) and Python 3.11+ (Engine & Crawlers)

FROM node:22-slim

# Install Python 3 and basic build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-minimal \
    python3-pip \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Alias python to python3
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /app

# Copy package descriptors
COPY package*.json ./

# Install npm dependencies
RUN npm ci

# Copy application source code
COPY . .

# Build the Vite React production bundle into dist/
RUN npm run build

# Initialize SQLite database and baseline artifacts
RUN python -m engine.cli init --no-live-audit

# Default production environment variables
ENV NODE_ENV=production
ENV PORT=3001
ENV SQLITE_DB_PATH=/app/data/incubrix.db

# Expose single application port
EXPOSE 3001

# Start production server (serves both /api and React frontend on PORT)
CMD ["npm", "run", "start:prod"]
