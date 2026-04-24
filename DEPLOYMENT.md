# 🚀 Deployment Guide

## Production Deployment Guide for Micro-Influencer Discovery System

This guide covers deploying the application to various platforms for production use.

---

## 📋 Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] No hardcoded secrets or credentials
- [ ] All `.env` variables are set correctly
- [ ] `USE_MOCK_DATA=false` (using real APIs)
- [ ] `DEBUG=false` (debug mode disabled)
- [ ] `ENVIRONMENT=production`
- [ ] Log level is `INFO` or `WARNING`
- [ ] SSL/TLS certificate is ready
- [ ] Database is configured (if applicable)
- [ ] Email credentials are verified
- [ ] API keys have appropriate rate limits
- [ ] Monitoring and alerting is configured
- [ ] Backup and recovery plan is in place

---

## 🐳 Docker Deployment

### Option 1: Traditional Docker

#### Step 1: Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Step 2: Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
.env
.env.*
logs/
.pytest_cache/
htmlcov/
.coverage
*.db
.DS_Store
```

#### Step 3: Build and Run

```bash
# Build image
docker build -t micro-influencer-system:latest .

# Run container
docker run -d \
  --name micro-influencer \
  -p 8000:8000 \
  -e YOUTUBE_API_KEY=$YOUTUBE_API_KEY \
  -e SMTP_EMAIL=$SMTP_EMAIL \
  -e SMTP_PASSWORD=$SMTP_PASSWORD \
  -e ENVIRONMENT=production \
  -e USE_MOCK_DATA=false \
  -v $(pwd)/logs:/app/logs \
  micro-influencer-system:latest

# Check logs
docker logs -f micro-influencer
```

### Option 2: Docker Compose

#### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      YOUTUBE_API_KEY: ${YOUTUBE_API_KEY}
      SMTP_EMAIL: ${SMTP_EMAIL}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      ENVIRONMENT: production
      USE_MOCK_DATA: "false"
      LOG_LEVEL: INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add MongoDB for persistent storage
  # mongo:
  #   image: mongo:6.0
  #   ports:
  #     - "27017:27017"
  #   volumes:
  #     - mongo_data:/data/db
  #   environment:
  #     MONGO_INITDB_ROOT_USERNAME: admin
  #     MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}

volumes:
  # mongo_data:
```

#### Run with Docker Compose

```bash
# Create .env.production file
cp .env.example .env.production
# Edit .env.production with real credentials

# Start services
docker-compose --env-file .env.production up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## ☁️ Cloud Deployment

### Option A: Heroku (Free Alternative)

#### Step 1: Install Heroku CLI
```bash
# Visit: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Create Heroku App
```bash
heroku login
heroku create micro-influencer-system
```

#### Step 3: Add Procfile
```procfile
# Procfile
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

#### Step 4: Set Environment Variables
```bash
heroku config:set YOUTUBE_API_KEY=your_key
heroku config:set SMTP_EMAIL=your_email
heroku config:set SMTP_PASSWORD=your_password
heroku config:set ENVIRONMENT=production
heroku config:set USE_MOCK_DATA=false
```

#### Step 5: Deploy
```bash
git push heroku main
```

#### Step 6: View Logs
```bash
heroku logs -t
heroku open
```

### Option B: AWS (Scalable)

#### Using Elastic Beanstalk

##### Step 1: Install EB CLI
```bash
pip install awsebcli
```

##### Step 2: Initialize EB Environment
```bash
eb init -p python-3.10 micro-influencer
```

##### Step 3: Create Application
```bash
eb create production-env
```

##### Step 4: Set Environment Variables
```bash
eb setenv YOUTUBE_API_KEY=your_key ENVIRONMENT=production USE_MOCK_DATA=false
```

##### Step 5: Deploy
```bash
eb deploy
```

##### Step 6: Monitor
```bash
eb status
eb logs
eb open
```

### Option C: Google Cloud Run

#### Step 1: Authenticate
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Step 2: Build Image
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/micro-influencer
```

#### Step 3: Deploy Service
```bash
gcloud run deploy micro-influencer \
  --image gcr.io/YOUR_PROJECT_ID/micro-influencer \
  --platform managed \
  --region us-central1 \
  --set-env-vars YOUTUBE_API_KEY=your_key,ENVIRONMENT=production
```

#### Step 4: Check Deployment
```bash
gcloud run services list
gcloud run services describe micro-influencer --region us-central1
```

---

## 🔐 Production Security Setup

### 1. Environment Variables

```bash
# Use AWS Secrets Manager, Google Secret Manager, or similar
# Never commit .env to git

# .gitignore should include:
.env
.env.production
.env.local
credentials/
*.key
*.pem
```

### 2. HTTPS/SSL Setup

#### Using Let's Encrypt (Free)

```bash
# Install certbot
pip install certbot

# Get certificate
certbot certonly --standalone -d yourdomain.com

# Update Uvicorn config to use SSL
uvicorn backend.main:app \
  --ssl-keyfile=/etc/letsencrypt/live/yourdomain.com/privkey.pem \
  --ssl-certfile=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
```

### 3. API Rate Limiting

```python
# In backend/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/discover")
@limiter.limit("100/hour")  # 100 requests per hour
async def discover_influencers(request: DiscoverRequest):
    ...
```

### 4. CORS Configuration

```python
# In backend/main.py
from fastapi.middleware.cors import CORSMiddleware

# In production, restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 5. Database Security

```python
# Use secure connection strings
MONGODB_URL = os.getenv("MONGODB_URL")  # From secure storage
# Never hardcode database credentials
```

---

## 📊 Monitoring & Logging

### Setup Structured Logging

```bash
# Install logging services
pip install python-json-logger

# Example: Send logs to CloudWatch, Datadog, or similar
```

### Health Check Monitoring

```bash
# Setup monitoring service to ping /api/health
# Example: Datadog, New Relic, Sentry

# Add monitoring to requirements-dev.txt
sentry-sdk==1.40.0
```

### Performance Monitoring

```python
# In backend/main.py
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('requests_total', 'Total requests')
request_latency = Histogram('request_latency_seconds', 'Request latency')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    request_count.inc()
    start = time.time()
    response = await call_next(request)
    request_latency.observe(time.time() - start)
    return response
```

---

## 🗄️ Database Setup

### MongoDB Atlas (Cloud)

```python
# .env
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/database?retryWrites=true&w=majority

# Code
from pymongo import MongoClient

client = MongoClient(MONGODB_URL)
db = client.micro_influencers
creators_collection = db.creators

# Save results
creators_collection.insert_many(scored_creators)
```

### PostgreSQL (Traditional)

```python
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/micro_influencers

# Code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: pytest tests/ -v --cov=backend

    - name: Build Docker image
      run: |
        docker build -t micro-influencer:${{ github.sha }} .
        docker tag micro-influencer:${{ github.sha }} micro-influencer:latest

    - name: Push to registry
      run: |
        # Push to Docker Hub, ECR, or GCR
        docker push micro-influencer:latest

    - name: Deploy to production
      run: |
        # Deploy using Heroku, AWS, GCP, or other service
        # Example:
        # gcloud run deploy ...
        echo "Deploying to production"
```

---

## 🔍 Verification Checklist

After deployment, verify:

- [ ] API is accessible at `yourdomain.com/api/health`
- [ ] Swagger docs work: `yourdomain.com/docs`
- [ ] Environment variables are set correctly
- [ ] Logs are being generated and accessible
- [ ] HTTPS is working and redirecting
- [ ] Database connection is working
- [ ] Email sending is working
- [ ] API rate limiting is active
- [ ] CORS headers are correct
- [ ] SSL certificate is valid

---

## 🆘 Troubleshooting

### Issue: Port already in use
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

### Issue: Docker container exits immediately
```bash
docker logs container_id
docker run -it image_id /bin/bash  # Interactive debug
```

### Issue: API returns 502 Bad Gateway
```bash
# Check Docker logs
docker logs container_id

# Check process is running
curl localhost:8000/api/health

# Restart container
docker restart container_id
```

### Issue: Rate limit errors
```
# Increase rate limit in settings
RATE_LIMIT=1000/hour
```

### Issue: Database connection timeout
```
# Check connection string
# Verify firewall rules
# Check database is running
```

---

## 📈 Scaling for Production

### Horizontal Scaling

```yaml
# docker-compose.yml with load balancer
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

  api1:
    build: .
    environment:
      WORKER_ID: 1

  api2:
    build: .
    environment:
      WORKER_ID: 2

  api3:
    build: .
    environment:
      WORKER_ID: 3
```

### Vertical Scaling

```bash
# Increase workers
uvicorn backend.main:app --workers 8

# Increase resources in Docker
docker run -m 2g --cpus 2 ...
```

---

## 📞 Support

For deployment issues:
1. Check logs: `docker logs container_id`
2. Review error messages carefully
3. Verify all environment variables
4. Test locally first
5. Check security group/firewall rules

---

**Last Updated:** April 24, 2026  
**Version:** 1.0.0
