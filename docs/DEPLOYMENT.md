# Deployment Guide

This guide covers deploying the SmartPass application to production environments.

## Prerequisites

- Docker and Docker Compose
- Domain name (optional)
- SSL certificate (recommended for production)

## Environment Configuration

### Production Environment Variables

Create a `.env` file in the server directory with production values:

```env
# Database
DATABASE_URL=postgresql://smartpass:secure_password@db:5432/smartpass

# Security
SECRET_KEY=your-very-secure-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ML Model
MODEL_PATH=/app/ml/models/fraud_model.pkl
```

## Docker Deployment

### 1. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.backend
    environment:
      - DATABASE_URL=postgresql://smartpass:${DB_PASSWORD}@db:5432/smartpass
      - SECRET_KEY=${SECRET_KEY}
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=60
    depends_on:
      - db
    volumes:
      - ./ml/models:/app/ml/models:ro
    networks:
      - smartpass-network
    restart: unless-stopped

  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    environment:
      - VITE_API_URL=https://api.yourdomain.com
    depends_on:
      - backend
    networks:
      - smartpass-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=smartpass
      - POSTGRES_USER=smartpass
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - smartpass-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - backend
      - frontend
    networks:
      - smartpass-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  smartpass-network:
    driver: bridge
```

### 2. Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;

    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:5173;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api/ {
            limit_req zone=api burst=20 nodelay;

            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # CORS headers
            add_header 'Access-Control-Allow-Origin' 'https://yourdomain.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;

            if ($request_method = 'OPTIONS') {
                return 204;
            }
        }

        # Static files
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 3. SSL Certificate Setup

Use Let's Encrypt for free SSL certificates:

```bash
# Install certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx/ssl directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./nginx/ssl/
```

## Deployment Steps

### 1. Prepare the Server

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/smartpass
cd /opt/smartpass
```

### 2. Clone and Configure

```bash
# Clone repository
git clone <your-repo-url> .
cd SmartPass

# Create environment file
cp server/.env.example server/.env
nano server/.env  # Edit with production values

# Generate secure secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Database Initialization

```bash
# Create init script
mkdir -p scripts
cat > scripts/init.sql << EOF
-- Database initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOF
```

### 4. Deploy

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up --build -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python scripts/run_migrations.py

# Seed initial data
docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_data.py

# Train ML model
docker-compose -f docker-compose.prod.yml exec backend python scripts/train_model.py
```

### 5. Verify Deployment

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Test API
curl https://yourdomain.com/api/docs
```

## Monitoring and Maintenance

### Health Checks

Add health check endpoints to your monitoring system:

```bash
# Backend health check
curl https://yourdomain.com/api/health

# Database connectivity
docker-compose -f docker-compose.prod.yml exec backend python -c "
from app.database import SessionLocal
db = SessionLocal()
db.execute('SELECT 1')
print('Database OK')
"
```

### Backup Strategy

```bash
# Database backup script
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/smartpass/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U smartpass smartpass > $BACKUP_DIR/smartpass_$DATE.sql

# Backup ML models
cp -r ml/models $BACKUP_DIR/models_$DATE

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "models_*" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/smartpass_$DATE.sql"
EOF

chmod +x scripts/backup.sh

# Add to crontab for daily backups
echo "0 2 * * * /opt/smartpass/scripts/backup.sh" | crontab -
```

### Log Rotation

```bash
# Install logrotate
sudo apt-get install logrotate

# Create logrotate config
cat > /etc/logrotate.d/smartpass << EOF
/opt/smartpass/nginx/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        docker-compose -f /opt/smartpass/docker-compose.prod.yml exec nginx nginx -s reload
    endscript
}
EOF
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Use load balancer
# Update nginx config to include multiple backend servers
upstream backend {
    server backend:8000;
    server backend:8001;
    server backend:8002;
}
```

### Database Scaling

For high-traffic applications, consider:
- Database read replicas
- Connection pooling (PgBouncer)
- Database sharding

## Troubleshooting

### Common Issues

1. **Container fails to start**
   ```bash
   docker-compose -f docker-compose.prod.yml logs <service_name>
   ```

2. **Database connection issues**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python -c "
   from app.database import engine
   from sqlalchemy import text
   with engine.connect() as conn:
       result = conn.execute(text('SELECT 1'))
       print('DB connection OK')
   "
   ```

3. **SSL certificate renewal**
   ```bash
   # Renew certificates
   sudo certbot renew

   # Reload nginx
   docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
   ```

4. **Memory issues**
   ```bash
   # Check container resource usage
   docker stats

   # Add memory limits to docker-compose
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 1G
           reservations:
             memory: 512M
   ```

## Security Considerations

- Keep Docker and dependencies updated
- Use strong passwords and secure secret keys
- Implement proper firewall rules
- Regularly audit access logs
- Enable fail2ban for brute force protection
- Use HTTPS everywhere
- Implement rate limiting
- Regular security scans with tools like Clair or Trivy