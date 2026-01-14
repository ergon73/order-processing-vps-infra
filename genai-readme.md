# 🤖 CURSOR AGENT SPECIFICATION (AUTO MODE)
## VPS Infrastructure Deployment - Order Processing System

> **CRITICAL**: This document is for Cursor Agent in AUTO mode.  
> Execute steps STRICTLY in order. NO additional services. NO deviations.

---

## 📋 CONTEXT & CONSTRAINTS

### Environment
- **Local OS**: Windows 11 (Cursor client)
- **Remote VPS**: Ubuntu 22.04 (via Remote-SSH, user: `root`)
- **Connection**: Cursor Remote-SSH extension
- **Working Directory**: `/root/order-processing-vps-infra/`

### Goal
Deploy Docker Compose infrastructure with:
- Nginx (web server, reverse proxy)
- PostgreSQL (database)
- pgAdmin (database UI)
- Watchtower (auto-updates)
- Private Docker Registry (with htpasswd auth)

### Security Requirements (MANDATORY)
- ❌ NEVER output/log:
  - Private SSH keys
  - `.env` file contents
  - Passwords/tokens/secrets
  - `registry/auth/htpasswd` contents
- ❌ NEVER commit:
  - `.env` (only `.env.example`)
  - `registry/auth/htpasswd`
  - `nginx/ssl/*`
  - Any SSH keys

---

## 🎯 ACCEPTANCE CRITERIA

### Step 1: VPS Check
```bash
docker compose up -d
docker ps
```
Expected: All containers status `Up`:
- nginx
- postgres
- pgadmin
- registry
- watchtower

### Step 2: Registry Auth
```bash
ls -l registry/auth/htpasswd  # File exists
curl -u <USER>:<PASS> http://127.0.0.1:5000/v2/
```
Expected response: `{}`

### Step 3: pgAdmin Access
Browser: `http://<VPS_IP>:5050`
Expected: pgAdmin login screen

### Step 4: Nginx Check
Browser: `http://<VPS_IP>/`
Expected: Static HTML page

---

## 📝 REQUIRED FILE TREE

```
/root/order-processing-vps-infra/
├── docker-compose.yml
├── .env.example
├── .env                    # Created on VPS, NOT committed
├── .gitignore
├── .cursorrules
├── README.md
├── human-readme.md
├── genai-readme.md         # This file
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/
│   │   └── default.conf
│   ├── html/
│   │   └── index.html
│   └── ssl/                # Empty directory
└── registry/
    ├── create-user.sh      # chmod +x
    └── auth/               # Empty directory
        └── htpasswd        # Created by script, NOT committed
```

---

## 🔧 STEP-BY-STEP EXECUTION PLAN

### STEP A: Diagnose VPS Environment

```bash
set -e
whoami
lsb_release -a || cat /etc/os-release
uname -a
```

**Expected**:
- User: `root`
- OS: Ubuntu 22.04
- Architecture: x86_64

---

### STEP B: Install Docker + docker compose plugin

#### B.1 - Check if Docker exists
```bash
docker version || echo "Docker not installed"
docker compose version || echo "Compose plugin not installed"
```

#### B.2 - Install Docker (if needed)
```bash
# Add Docker GPG key
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine + Compose plugin
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### B.3 - Verify Installation
```bash
docker version
docker compose version  # Must show v2.x.x
systemctl status docker --no-pager
```

**Expected**:
- Docker version: 20.10+
- Compose version: v2.x.x (plugin, NOT standalone binary)
- Docker service: active (running)

---

### STEP C: Create Project Directory

```bash
mkdir -p /root/order-processing-vps-infra
cd /root/order-processing-vps-infra
```

---

### STEP D: Create Project Files (EXACTLY as specified)

⚠️ **IMPORTANT**: Create files with EXACT content from the templates below.

#### D.1 - docker-compose.yml
```yaml
services:
  nginx:
    image: nginx:1.27-alpine
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/html:/usr/share/nginx/html:ro
    depends_on:
      - postgres
      - pgadmin
    networks:
      - frontend_network
      - backend_network
    restart: unless-stopped
    labels:
      - "com.centurylinklabs.watchtower.enable=true"

  postgres:
    image: postgres:16-alpine
    container_name: postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-app_db}
      POSTGRES_USER: ${POSTGRES_USER:-app_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-app_user}"]
      interval: 10s
      timeout: 5s
      retries: 5
    labels:
      - "com.centurylinklabs.watchtower.enable=true"

  pgadmin:
    image: dpage/pgadmin4:8.2
    container_name: pgadmin
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
      PGADMIN_CONFIG_SERVER_MODE: 'False'
      PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres
    networks:
      - backend_network
    restart: unless-stopped
    labels:
      - "com.centurylinklabs.watchtower.enable=true"

  registry:
    image: registry:2
    container_name: registry
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - registry_data:/var/lib/registry
      - ./registry/auth:/auth:ro
    networks:
      - backend_network
    restart: unless-stopped
    labels:
      - "com.centurylinklabs.watchtower.enable=true"

  watchtower:
    image: nickfedor/watchtower:latest  # Форк, совместимый с Docker 29 (API 1.44+)
    container_name: watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      WATCHTOWER_CLEANUP: "true"
      WATCHTOWER_POLL_INTERVAL: 300
      WATCHTOWER_LABEL_ENABLE: "true"
    networks:
      - backend_network
    restart: unless-stopped

networks:
  frontend_network:
    driver: bridge
  backend_network:
    driver: bridge
    internal: false

volumes:
  postgres_data:
    driver: local
  pgadmin_data:
    driver: local
  registry_data:
    driver: local
```

#### D.2 - .env.example
```env
# PostgreSQL
POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=CHANGE_ME_MIN_12_CHARS

# pgAdmin
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=CHANGE_ME_MIN_12_CHARS

# Notes:
# 1. Copy: cp .env.example .env
# 2. Replace all CHANGE_ME_* with strong passwords (12+ chars)
# 3. .env is in .gitignore
```

#### D.3 - .gitignore
```
.env
.env.local
registry/auth/htpasswd
nginx/ssl/*
*.pem
*.key
*.log
.DS_Store
.vscode/
```

#### D.4 - Directory Structure
```bash
mkdir -p nginx/conf.d nginx/html nginx/ssl
mkdir -p registry/auth

# nginx/nginx.conf - Create minimal config
# nginx/conf.d/default.conf - Create server block
# nginx/html/index.html - Create static page
# registry/create-user.sh - Create htpasswd script
```

⚠️ **DO NOT create** `registry/auth/htpasswd` in repo. It's created by script on VPS.

---

### STEP E: Create .env on VPS

```bash
cp .env.example .env
# User will fill manually OR generate temporary passwords for testing
```

⚠️ **DO NOT output passwords in chat. DO NOT commit .env.**

For quick test, generate secure passwords:
```bash
# POSTGRES_PASSWORD
openssl rand -base64 16

# PGADMIN_PASSWORD  
openssl rand -base64 16
```

Edit `.env` with generated values (user does this manually).

---

### STEP F: Create Registry User (htpasswd)

```bash
cd /root/order-processing-vps-infra/registry
chmod +x create-user.sh
./create-user.sh admin "<STRONG_PASSWORD>"
```

Verify file created:
```bash
ls -l auth/htpasswd
cat auth/htpasswd  # Should show bcrypt hash
```

---

### STEP G: Launch Compose Stack

```bash
cd /root/order-processing-vps-infra
docker compose config  # Validate syntax
docker compose up -d   # Start in background
docker ps              # Check status
```

**Expected**: All 5 containers in `Up` status:
- nginx
- postgres  
- pgadmin
- registry
- watchtower

If any container restarting:
```bash
docker compose logs --tail=200 <container_name>
```

---

### STEP H: Verification Tests

#### H.1 - Registry Access (Local on VPS)
```bash
curl -u admin:<PASSWORD> http://127.0.0.1:5000/v2/
```
Expected: `{}`

#### H.2 - pgAdmin (Browser)
URL: `http://<VPS_IP>:5050`
Login:
- Email: from `.env` (PGADMIN_EMAIL)
- Password: from `.env` (PGADMIN_PASSWORD)

Add server in pgAdmin:
- Host: `postgres`
- Port: `5432`
- Username: from `.env` (POSTGRES_USER)
- Password: from `.env` (POSTGRES_PASSWORD)

#### H.3 - Nginx (Browser)
URL: `http://<VPS_IP>/`
Expected: Static HTML page

---

## 🚫 FORBIDDEN ACTIONS

### DO NOT:
- Use `docker-compose` (old binary) - use `docker compose` (plugin)
- Expose Postgres port externally (no `5432:5432` in compose)
- Commit `.env`, `htpasswd`, certificates, private keys
- Disable SSH host key checking (`StrictHostKeyChecking no`)
- Add extra services not in requirements (Redis, Traefik, etc.)
- Execute mass deletions without confirmation
- Modify firewall rules without user request

---

## 📦 Git Operations (if local repo)

If working in local Windows repository:
```bash
git init
git add -A
git commit -m "Initial infrastructure: nginx/postgres/pgadmin/registry/watchtower"
```

User pushes to GitHub manually.

---

## 🔍 TROUBLESHOOTING COMMANDS

### Container restarting
```bash
docker compose logs --tail=200 <service>
docker compose down <service>
docker compose up -d <service>
```

### Registry not authenticating
```bash
ls -l registry/auth/htpasswd
docker compose restart registry
```

### Docker daemon issues
```bash
systemctl status docker
systemctl restart docker
journalctl -u docker -n 50
```

### Disk space
```bash
df -h
docker system df
docker system prune -a  # Clean unused resources
```

---

## ✅ SUCCESS CRITERIA CHECKLIST

- [ ] Docker Engine installed (v20.10+)
- [ ] docker compose plugin installed (v2.x+)
- [ ] All project files created
- [ ] `.env` configured (passwords set)
- [ ] Registry htpasswd file created
- [ ] All containers running (`docker ps`)
- [ ] Registry accessible: `curl -u user:pass http://127.0.0.1:5000/v2/` → `{}`
- [ ] pgAdmin accessible: `http://<VPS_IP>:5050`
- [ ] Nginx accessible: `http://<VPS_IP>/`
- [ ] No secrets in git history
- [ ] `.gitignore` properly configured

---

## 📞 FINAL NOTES

- This is Step 1 of the project. Backend will be added in Part 2.
- For production: hide pgAdmin/Registry behind VPN or restrict by IP.
- Always use `docker compose` (plugin), never `docker-compose` (legacy).
- When user says "It's not working" - ask for specific error logs.

---

**End of Agent Specification**
