# 🏗️ VPS Infrastructure for Order Processing System

[![Docker](https://img.shields.io/badge/Docker-v20.10+-blue.svg)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v2.0+-blue.svg)](https://docs.docker.com/compose/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20LTS-orange.svg)](https://ubuntu.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Production-ready VPS infrastructure for order processing web application. Deployed via Docker Compose on Ubuntu 22.04 VPS with Nginx, PostgreSQL, pgAdmin, private Docker Registry, and automated updates.

> 🎓 **Educational Project**: Part of "Vibe-Coding" course - Module 8, Case 3  
> Demonstrates modern DevOps practices: Docker containerization, secure SSH access, infrastructure as code.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Services & Ports](#-services--ports)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🐳 Fully Dockerized**: All services run in Docker containers
- **🔐 Secure by Default**: PostgreSQL isolated in internal network, SSH key-only access
- **📦 Private Registry**: Self-hosted Docker registry with htpasswd authentication
- **🔄 Auto-Updates**: Watchtower automatically updates containers
- **⚡ Nginx Reverse Proxy**: High-performance web server and load balancer
- **🎛️ Database Management**: Web-based pgAdmin interface
- **📊 Production-Ready**: Healthchecks, restart policies, volume persistence

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        VPS (Ubuntu 22.04)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Docker Compose                      │  │
│  │                                                        │  │
│  │  ┌────────────┐     ┌──────────────┐                 │  │
│  │  │   Nginx    │────▶│  PostgreSQL  │                 │  │
│  │  │  (Port 80) │     │   (Internal) │                 │  │
│  │  └────────────┘     └──────────────┘                 │  │
│  │        │                    │                         │  │
│  │        │              ┌─────▼──────┐                 │  │
│  │        │              │  pgAdmin   │                 │  │
│  │        │              │ (Port 5050)│                 │  │
│  │        │              └────────────┘                 │  │
│  │        │                                              │  │
│  │  ┌─────▼──────┐     ┌──────────────┐                │  │
│  │  │  Registry  │     │  Watchtower  │                │  │
│  │  │(Port 5000) │     │(Auto-Update) │                │  │
│  │  └────────────┘     └──────────────┘                │  │
│  │                                                        │  │
│  │  [Frontend Network] ←→ [Backend Network]             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key Principles**:
- **Nginx** = Public entrypoint (port 80), serves static files, proxies requests
- **PostgreSQL** = Database, NO external ports, only accessible via Docker internal network
- **pgAdmin** = Database UI, port 5050 (restrict in production!)
- **Registry** = Private Docker image storage, port 5000 with htpasswd auth
- **Watchtower** = Monitors and updates containers automatically

---

## 🛠️ Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Server** | Nginx | 1.27-alpine | Reverse proxy, static files |
| **Database** | PostgreSQL | 16-alpine | Data persistence |
| **DB Admin** | pgAdmin 4 | 8.2 | Database management UI |
| **Container Registry** | Docker Registry | 2 | Private image storage |
| **Auto-Updater** | Watchtower (nickfedor fork) | latest | Container lifecycle (Docker 29 compatible) |
| **Orchestration** | Docker Compose | v2+ | Service management |
| **OS** | Ubuntu Server | 22.04 LTS | VPS operating system |

---

## 📋 Prerequisites

### Local Machine (Windows 11)
- **Cursor IDE** with Remote-SSH extension
- **SSH client** (built-in in Windows 10/11)
- **Git** (for cloning repository)

### VPS Server
- **Ubuntu 22.04 LTS** (minimal 1 CPU, 768 MB RAM, 7 GB SSD)
- **Public IPv4 address**
- **Root access** (or sudo user)
- **Open ports**: 22 (SSH), 80 (HTTP), 5000 (Registry), 5050 (pgAdmin)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/order-processing-vps-infra.git
cd order-processing-vps-infra
```

### 2. Configure Environment

```bash
cp .env.example .env
nano .env
```

Set strong passwords (12+ characters):
```env
POSTGRES_PASSWORD=your_strong_password_here
PGADMIN_PASSWORD=another_strong_password
```

### 3. Create Registry User

```bash
cd registry
chmod +x create-user.sh
./create-user.sh admin "YourRegistryPassword"
cd ..
```

### 4. Launch Services

```bash
docker compose up -d
```

### 5. Verify Deployment

```bash
docker ps  # All containers should be "Up"
```

**Access Services**:
- Web: `http://<VPS_IP>/`
- pgAdmin: `http://<VPS_IP>:5050`
- Registry: `http://<VPS_IP>:5000/v2/`

---

## 🔌 Services & Ports

| Service | Container Name | Internal Port | External Port | Access |
|---------|---------------|---------------|---------------|--------|
| **Nginx** | `nginx` | 80 | 80 | Public |
| **PostgreSQL** | `postgres` | 5432 | ❌ Not exposed | Internal only |
| **pgAdmin** | `pgadmin` | 80 | 5050 | Public (dev) |
| **Registry** | `registry` | 5000 | 5000 | Public (auth) |
| **Watchtower** | `watchtower` | - | - | Background |

⚠️ **Production Security**: In production environments, restrict `5050` and `5000` to VPN/trusted IPs only.

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# PostgreSQL Configuration
POSTGRES_DB=app_db          # Database name
POSTGRES_USER=app_user      # Database user
POSTGRES_PASSWORD=***       # Database password (CHANGE!)

# pgAdmin Configuration
PGADMIN_EMAIL=admin@example.com    # pgAdmin login email
PGADMIN_PASSWORD=***               # pgAdmin password (CHANGE!)
```

### Docker Compose Services

Edit `docker-compose.yml` to customize:
- **Resource limits**: Add `deploy.resources.limits` for CPU/memory
- **Networks**: Modify network configurations
- **Volumes**: Change volume mount paths
- **Environment**: Add service-specific env vars

### Nginx Configuration

- **Main config**: `nginx/nginx.conf`
- **Server blocks**: `nginx/conf.d/default.conf`
- **Static files**: `nginx/html/`

Example: Add HTTPS (requires SSL certificates):
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of config
}
```

---

## 📦 Deployment

### Initial Deployment

```bash
# On VPS
mkdir -p /root/order-processing-vps-infra
cd /root/order-processing-vps-infra

# Copy files or clone repo
git clone <repo_url> .

# Setup
cp .env.example .env
nano .env  # Fill passwords
cd registry && ./create-user.sh admin "password" && cd ..

# Launch
docker compose up -d
```

### Updating Services

```bash
docker compose pull          # Pull latest images
docker compose up -d         # Recreate updated containers
```

Or let Watchtower do it automatically (every 5 minutes).

### Backup Database

```bash
docker exec postgres pg_dump -U app_user app_db > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker exec -i postgres psql -U app_user app_db
```

---

## 🔐 Security

### Implemented Measures

✅ **PostgreSQL**: No external ports, only internal Docker network  
✅ **SSH**: Key-based authentication, password login disabled  
✅ **Registry**: htpasswd authentication  
✅ **Secrets**: `.env` file excluded from git  
✅ **Healthchecks**: Automatic service monitoring  
✅ **Least Privilege**: Containers run as non-root where possible  

### Production Recommendations

🔒 **Enable HTTPS**: Use Let's Encrypt for SSL certificates  
🔒 **Firewall**: Restrict ports with `ufw` or cloud provider firewall  
🔒 **VPN/Bastion**: Hide pgAdmin/Registry behind VPN or SSH tunnel  
🔒 **Monitoring**: Add Prometheus + Grafana for metrics  
🔒 **Backups**: Automated daily PostgreSQL backups  
🔒 **Secrets Management**: Use Docker Secrets or Vault  

---

## 🐛 Troubleshooting

### Container Restarting

```bash
# Check logs
docker compose logs --tail=200 <service_name>

# Common issues:
# - postgres: Wrong POSTGRES_PASSWORD in .env
# - registry: Missing auth/htpasswd file
# - pgadmin: Wrong PGADMIN_PASSWORD
```

### Registry Auth Failing

```bash
# Verify htpasswd file exists
ls -l registry/auth/htpasswd

# Recreate user
cd registry
rm auth/htpasswd
./create-user.sh admin "new_password"
docker compose restart registry
```

### pgAdmin Can't Connect to PostgreSQL

- **Host** must be `postgres` (container name), NOT `localhost` or `127.0.0.1`
- **Port** is `5432`
- Verify both containers in same network:
  ```bash
  docker network inspect order-processing-vps-infra_backend_network
  ```

### No Space Left

```bash
df -h                    # Check disk usage
docker system df         # Check Docker usage
docker system prune -a   # Clean unused resources
```

### Watchtower Compatibility

**Note**: This project uses `nickfedor/watchtower` fork instead of the original `containrrr/watchtower` because:
- Original Watchtower was archived (Dec 17, 2025) and incompatible with Docker 29
- The fork supports Docker API 1.44+ required for Docker 29
- All functionality remains the same (auto-updates every 5 minutes)

If you see API version errors with Watchtower, ensure you're using the fork:
```bash
# Check current image
docker compose config | grep watchtower

# Should show: image: nickfedor/watchtower:latest
```

---

## 📁 Project Structure

```
order-processing-vps-infra/
├── docker-compose.yml          # Main orchestration file
├── .env.example                # Environment template
├── .env                        # Actual secrets (not in git)
├── .gitignore                  # Git exclusions
├── .cursorrules                # Cursor AI rules
├── README.md                   # This file
├── human-readme.md             # Detailed setup guide (RU)
├── genai-readme.md             # Cursor Agent spec
├── nginx/
│   ├── nginx.conf              # Nginx main config
│   ├── conf.d/
│   │   └── default.conf        # Server block config
│   ├── html/
│   │   └── index.html          # Static landing page
│   └── ssl/                    # SSL certificates (not in git)
└── registry/
    ├── create-user.sh          # Registry user creation script
    └── auth/
        └── htpasswd            # Registry credentials (not in git)
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

**Code Style**:
- Use shellcheck for bash scripts
- Validate YAML with yamllint
- Test locally before PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Georgy**  
Student @ Vibe-Coding Course  
📧 Contact: [GitHub Profile](https://github.com/<YOUR_USERNAME>)

---

## 🙏 Acknowledgments

- **Course**: [ZeroCoder - Vibe-Coding](https://zerocoder.ru)
- **Instructor**: Module 8 - Business Process Automation
- **Tools**: Docker, Nginx, PostgreSQL, Watchtower

---

## 📊 Project Status

✅ **Stage 1**: Infrastructure setup (nginx, postgres, pgadmin, registry, watchtower)  
🔜 **Stage 2**: Backend application deployment (coming soon)  
🔜 **Stage 3**: Frontend integration & admin panel

---

**⭐ If this project helped you, please give it a star!**
