# 🏗️ VPS Infrastructure for Order Processing System

[![Docker](https://img.shields.io/badge/Docker-v20.10+-blue.svg)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v2.0+-blue.svg)](https://docs.docker.com/compose/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20LTS-orange.svg)](https://ubuntu.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**🇬🇧 [English](#-english) | [🇷🇺 Русский](#-русский)**

---

## 🇬🇧 English

Production-ready VPS infrastructure and web application for order processing. Full-stack solution with FastAPI backend, modern frontend, and PostgreSQL database. Deployed via Docker Compose on Ubuntu 22.04 VPS with Nginx, PostgreSQL, pgAdmin, private Docker Registry, and automated updates.

> 🎓 **Educational Project**: Part of "Vibe-Coding" course - Module 8, Case 3 (Part 2)  
> Demonstrates modern DevOps practices: Docker containerization, secure SSH access, infrastructure as code, RESTful API, and frontend build pipelines.

---

### 📋 Table of Contents

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

### ✨ Features

- **🐳 Fully Dockerized**: All services run in Docker containers
- **🚀 Full-Stack Application**: FastAPI backend + Webpack frontend
- **🎨 Modern UI**: "Elite style" frontend with smooth animations and elegant design
- **📡 RESTful API**: FastAPI with automatic OpenAPI/Swagger documentation
- **🗄️ Database**: PostgreSQL with SQLAlchemy ORM
- **🔐 Secure by Default**: PostgreSQL isolated in internal network, SSH key-only access
- **📦 Private Registry**: Self-hosted Docker registry with htpasswd authentication
- **🔄 Auto-Updates**: Watchtower automatically updates containers
- **⚡ Nginx Reverse Proxy**: High-performance web server, API proxy, and static file serving
- **🎛️ Database Management**: Web-based pgAdmin interface
- **📊 Production-Ready**: Healthchecks, restart policies, volume persistence

---

### 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        VPS (Ubuntu 22.04)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Docker Compose                      │  │
│  │                                                        │  │
│  │           ┌──────────────────────┐                   │  │
│  │           │   Nginx (Port 80)    │                   │  │
│  │           │  Reverse Proxy +     │                   │  │
│  │           │  Static Files        │                   │  │
│  │           └────┬─────────────┬───┘                   │  │
│  │                │             │                        │  │
│  │    Static      │             │ /api/*                 │  │
│  │  (frontend/)   │             ▼                        │  │
│  │                │    ┌──────────────────┐             │  │
│  │                │    │  FastAPI Backend │             │  │
│  │                │    │  (Private :8000) │             │  │
│  │                │    └─────────┬────────┘             │  │
│  │                │              │                       │  │
│  │                │              │ SQL                   │  │
│  │                │              ▼                       │  │
│  │                │    ┌──────────────────┐             │  │
│  │                │    │   PostgreSQL     │             │  │
│  │                │    │   (Internal)     │             │  │
│  │                │    └────────┬─────────┘             │  │
│  │                │             │                        │  │
│  │                │      ┌──────▼──────┐                │  │
│  │                │      │  pgAdmin    │                │  │
│  │                │      │ (Port 5050) │                │  │
│  │                │      └─────────────┘                │  │
│  │                │                                      │  │
│  │        ┌───────▼──────┐     ┌──────────────┐        │  │
│  │        │  Registry    │     │  Watchtower  │        │  │
│  │        │(Port 5000)   │     │(Auto-Update) │        │  │
│  │        └──────────────┘     └──────────────┘        │  │
│  │                                                        │  │
│  │  [Frontend Network] ←→ [Backend Network]             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key Principles**:
- **Nginx** = Public entrypoint (port 80), serves static files from `frontend/dist/`, proxies `/api/*` to backend
- **FastAPI Backend** = RESTful API (private :8000), not exposed externally
- **Frontend** = Webpack-built static files, "elite style" design
- **PostgreSQL** = Database, NO external ports, only accessible via Docker internal network
- **pgAdmin** = Database UI, port 5050 (restrict in production!)
- **Registry** = Private Docker image storage, port 5000 with htpasswd auth
- **Watchtower** = Monitors and updates containers automatically

---

### 🛠️ Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend** | FastAPI | latest | RESTful API, OpenAPI/Swagger docs |
| **Backend Language** | Python | 3.11 | Backend application logic |
| **ORM** | SQLAlchemy | latest | Database ORM |
| **Frontend** | Webpack + Vanilla JS | 5.x | Frontend build tool |
| **Frontend Runtime** | Node.js | 20+ | Frontend build environment |
| **Web Server** | Nginx | 1.27-alpine | Reverse proxy, static files |
| **Database** | PostgreSQL | 16-alpine | Data persistence |
| **DB Admin** | pgAdmin 4 | 8.2 | Database management UI |
| **Container Registry** | Docker Registry | 2 | Private image storage |
| **Auto-Updater** | Watchtower (nickfedor fork) | latest | Container lifecycle (Docker 29 compatible) |
| **Orchestration** | Docker Compose | v2+ | Service management |
| **OS** | Ubuntu Server | 22.04 LTS | VPS operating system |

---

### 📋 Prerequisites

#### Local Machine (Windows 11)
- **Cursor IDE** with Remote-SSH extension
- **SSH client** (built-in in Windows 10/11)
- **Git** (for cloning repository)

#### VPS Server
- **Ubuntu 22.04 LTS** (recommended 2 CPU, 2 GB RAM, 10 GB SSD)
- **Public IPv4 address**
- **Root access** (or sudo user)
- **Open ports**: 22 (SSH), 80 (HTTP), 5000 (Registry), 5050 (pgAdmin)
- **Node.js 20+** and **npm** (for frontend build)

---

### 🚀 Quick Start

#### 1. Clone Repository

```bash
git clone https://github.com/ergon73/order-processing-vps-infra.git
cd order-processing-vps-infra
```

#### 2. Configure Environment

```bash
cp .env.example .env
nano .env
```

Set strong passwords (12+ characters):
```env
POSTGRES_PASSWORD=your_strong_password_here
PGADMIN_PASSWORD=another_strong_password
```

#### 3. Create Registry User

```bash
cd registry
chmod +x create-user.sh
./create-user.sh admin "YourRegistryPassword"
cd ..
```

#### 4. Build Frontend

```bash
cd frontend
npm ci
npm run build
cd ..
```

#### 5. Launch Services

```bash
docker compose up -d --build
```

#### 6. Verify Deployment

```bash
docker compose ps  # All containers should be "Up"
```

**Access Services**:
- **Frontend**: `http://<VPS_IP>/`
- **Swagger UI**: `http://<VPS_IP>/api/docs`
- **API**: `http://<VPS_IP>/api/`
- **pgAdmin**: `http://<VPS_IP>:5050`
- **Registry**: `http://<VPS_IP>:5000/v2/`

---

### 🔌 Services & Ports

| Service | Container Name | Internal Port | External Port | Access |
|---------|---------------|---------------|---------------|--------|
| **Nginx** | `nginx` | 80 | 80 | Public |
| **PostgreSQL** | `postgres` | 5432 | ❌ Not exposed | Internal only |
| **pgAdmin** | `pgadmin` | 80 | 5050 | Public (dev) |
| **Registry** | `registry` | 5000 | 5000 | Public (auth) |
| **Watchtower** | `watchtower` | - | - | Background |

⚠️ **Production Security**: In production environments, restrict `5050` and `5000` to VPN/trusted IPs only.

---

### ⚙️ Configuration

#### Environment Variables (.env)

```env
# PostgreSQL Configuration
POSTGRES_DB=app_db          # Database name
POSTGRES_USER=app_user      # Database user
POSTGRES_PASSWORD=***       # Database password (CHANGE!)

# pgAdmin Configuration
PGADMIN_EMAIL=admin@example.com    # pgAdmin login email
PGADMIN_PASSWORD=***               # pgAdmin password (CHANGE!)
```

#### Docker Compose Services

Edit `docker-compose.yml` to customize:
- **Resource limits**: Add `deploy.resources.limits` for CPU/memory
- **Networks**: Modify network configurations
- **Volumes**: Change volume mount paths
- **Environment**: Add service-specific env vars

#### Nginx Configuration

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

### 📦 Deployment

#### Initial Deployment

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

#### Updating Services

```bash
docker compose pull          # Pull latest images
docker compose up -d         # Recreate updated containers
```

Or let Watchtower do it automatically (every 5 minutes).

#### Backup Database

```bash
docker exec postgres pg_dump -U app_user app_db > backup.sql
```

#### Restore Database

```bash
cat backup.sql | docker exec -i postgres psql -U app_user app_db
```

---

### 🔐 Security

#### Implemented Measures

✅ **PostgreSQL**: No external ports, only internal Docker network  
✅ **SSH**: Key-based authentication, password login disabled  
✅ **Registry**: htpasswd authentication  
✅ **Secrets**: `.env` file excluded from git  
✅ **Healthchecks**: Automatic service monitoring  
✅ **Least Privilege**: Containers run as non-root where possible  

#### Production Recommendations

🔒 **Enable HTTPS**: Use Let's Encrypt for SSL certificates  
🔒 **Firewall**: Restrict ports with `ufw` or cloud provider firewall  
🔒 **VPN/Bastion**: Hide pgAdmin/Registry behind VPN or SSH tunnel  
🔒 **Monitoring**: Add Prometheus + Grafana for metrics  
🔒 **Backups**: Automated daily PostgreSQL backups  
🔒 **Secrets Management**: Use Docker Secrets or Vault  

---

### 🐛 Troubleshooting

#### Container Restarting

```bash
# Check logs
docker compose logs --tail=200 <service_name>

# Common issues:
# - postgres: Wrong POSTGRES_PASSWORD in .env
# - registry: Missing auth/htpasswd file
# - pgadmin: Wrong PGADMIN_PASSWORD
```

#### Registry Auth Failing

```bash
# Verify htpasswd file exists
ls -l registry/auth/htpasswd

# Recreate user
cd registry
rm auth/htpasswd
./create-user.sh admin "new_password"
docker compose restart registry
```

#### pgAdmin Can't Connect to PostgreSQL

- **Host** must be `postgres` (container name), NOT `localhost` or `127.0.0.1`
- **Port** is `5432`
- Verify both containers in same network:
  ```bash
  docker network inspect order-processing-vps-infra_backend_network
  ```

#### No Space Left

```bash
df -h                    # Check disk usage
docker system df         # Check Docker usage
docker system prune -a   # Clean unused resources
```

#### Watchtower Compatibility

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

### 📁 Project Structure

```
order-processing-vps-infra/
├── docker-compose.yml          # Main orchestration file
├── .env.example                # Environment template
├── .env                        # Actual secrets (not in git)
├── .gitignore                  # Git exclusions
├── README.md                   # This file (main documentation)
├── nginx/
│   ├── nginx.conf              # Nginx main config
│   ├── conf.d/
│   │   └── default.conf        # Server block config (API proxy + static files)
│   └── ssl/                    # SSL certificates (not in git)
├── backend/                    # FastAPI backend application
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   └── database.py         # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── admin_settings.py
│   │   ├── applications.py
│   │   └── behavior_metrics.py
│   └── routes/                 # API routes
│       ├── admin_settings.py
│       └── applications.py
├── frontend/                   # Webpack frontend application
│   ├── package.json
│   ├── webpack.config.js
│   ├── src/
│   │   ├── index.html          # Main HTML template
│   │   ├── index.js            # Application logic
│   │   └── styles.css          # "Elite style" CSS
│   └── dist/                   # Build output (generated, not in git)
│       ├── index.html
│       ├── main.*.css          # Extracted CSS
│       └── main.*.js           # Bundled JavaScript
└── registry/
    ├── create-user.sh          # Registry user creation script
    └── auth/
        └── htpasswd            # Registry credentials (not in git)
```

---

### 🤝 Contributing

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

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 👤 Author

**Georgy**  
Student @ Vibe-Coding Course  
📧 Contact: [GitHub Profile](https://github.com/ergon73)

---

### 🙏 Acknowledgments

- **Course**: [ZeroCoder - Vibe-Coding](https://zerocoder.ru)
- **Instructor**: Module 8 - Business Process Automation
- **Tools**: Docker, Nginx, PostgreSQL, Watchtower

---

### 📊 Project Status

✅ **Stage 1**: Infrastructure setup (nginx, postgres, pgadmin, registry, watchtower)  
✅ **Stage 2**: Backend application deployment (FastAPI + PostgreSQL + SQLAlchemy)  
✅ **Stage 3**: Frontend integration (Webpack + Vanilla JS, "elite style" design)

**Current Version**: Part 2 - Full-stack application with backend and frontend

**Status**: ✅ **Production Ready** - All components functional, tested, and deployed

---

## 🇷🇺 Русский

Готовая к продакшену VPS инфраструктура и веб-приложение для обработки заказов. Полноценное full-stack решение с FastAPI backend, современным frontend и PostgreSQL базой данных. Развертывается через Docker Compose на Ubuntu 22.04 VPS с Nginx, PostgreSQL, pgAdmin, приватным Docker Registry и автоматическими обновлениями.

> 🎓 **Учебный проект**: Часть курса "Vibe-Coding" - Модуль 8, Кейс 3 (Часть 2)  
> Демонстрирует современные DevOps практики: контейнеризация Docker, безопасный SSH доступ, инфраструктура как код, RESTful API и frontend build pipelines.

---

### 📋 Содержание

- [Возможности](#-возможности)
- [Архитектура](#-архитектура)
- [Технологический стек](#-технологический-стек)
- [Требования](#-требования)
- [Быстрый старт](#-быстрый-старт)
- [Сервисы и порты](#-сервисы-и-порты)
- [Конфигурация](#-конфигурация)
- [Развертывание](#-развертывание)
- [Безопасность](#-безопасность)
- [Решение проблем](#-решение-проблем)
- [Структура проекта](#-структура-проекта)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)

---

### ✨ Возможности

- **🐳 Полная контейнеризация**: Все сервисы работают в Docker контейнерах
- **🚀 Full-Stack Приложение**: FastAPI backend + Webpack frontend
- **🎨 Современный UI**: "Элитный" дизайн frontend с плавными анимациями
- **📡 RESTful API**: FastAPI с автоматической документацией OpenAPI/Swagger
- **🗄️ База данных**: PostgreSQL с ORM SQLAlchemy
- **🔐 Безопасность по умолчанию**: PostgreSQL изолирован во внутренней сети, доступ только по SSH-ключу
- **📦 Приватный Registry**: Собственный Docker registry с аутентификацией htpasswd
- **🔄 Автообновления**: Watchtower автоматически обновляет контейнеры
- **⚡ Nginx Reverse Proxy**: Высокопроизводительный веб-сервер, проксирование API и раздача статики
- **🎛️ Управление БД**: Веб-интерфейс pgAdmin
- **📊 Готово к продакшену**: Healthchecks, политики перезапуска, персистентные тома

---

### 🏛️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                        VPS (Ubuntu 22.04)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Docker Compose                      │  │
│  │                                                        │  │
│  │           ┌──────────────────────┐                   │  │
│  │           │   Nginx (Порт 80)    │                   │  │
│  │           │  Reverse Proxy +     │                   │  │
│  │           │  Статические файлы   │                   │  │
│  │           └────┬─────────────┬───┘                   │  │
│  │                │             │                        │  │
│  │    Статика     │             │ /api/*                 │  │
│  │  (frontend/)   │             ▼                        │  │
│  │                │    ┌──────────────────┐             │  │
│  │                │    │  FastAPI Backend │             │  │
│  │                │    │  (Внутренний     │             │  │
│  │                │    │   :8000)         │             │  │
│  │                │    └─────────┬────────┘             │  │
│  │                │              │                       │  │
│  │                │              │ SQL                   │  │
│  │                │              ▼                       │  │
│  │                │    ┌──────────────────┐             │  │
│  │                │    │   PostgreSQL     │             │  │
│  │                │    │   (Внутренний)   │             │  │
│  │                │    └────────┬─────────┘             │  │
│  │                │             │                        │  │
│  │                │      ┌──────▼──────┐                │  │
│  │                │      │  pgAdmin    │                │  │
│  │                │      │ (Порт 5050) │                │  │
│  │                │      └─────────────┘                │  │
│  │                │                                      │  │
│  │        ┌───────▼──────┐     ┌──────────────┐        │  │
│  │        │  Registry    │     │  Watchtower  │        │  │
│  │        │(Порт 5000)   │     │(Автообновление)│        │  │
│  │        └──────────────┘     └──────────────┘        │  │
│  │                                                        │  │
│  │  [Frontend Network] ←→ [Backend Network]             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Ключевые принципы**:
- **Nginx** = Публичная точка входа (порт 80), отдает статические файлы из `frontend/dist/`, проксирует `/api/*` в backend
- **FastAPI Backend** = RESTful API (внутренний :8000), не открыт внешне
- **Frontend** = Собранные Webpack статические файлы, "элитный" дизайн
- **PostgreSQL** = База данных, БЕЗ внешних портов, доступна только через внутреннюю Docker сеть
- **pgAdmin** = UI для БД, порт 5050 (ограничить в продакшене!)
- **Registry** = Приватное хранилище Docker образов, порт 5000 с аутентификацией htpasswd
- **Watchtower** = Мониторит и автоматически обновляет контейнеры

---

### 🛠️ Технологический стек

| Компонент | Технология | Версия | Назначение |
|-----------|-----------|---------|------------|
| **Backend** | FastAPI | latest | RESTful API, документация OpenAPI/Swagger |
| **Язык Backend** | Python | 3.11 | Логика backend приложения |
| **ORM** | SQLAlchemy | latest | ORM для работы с БД |
| **Frontend** | Webpack + Vanilla JS | 5.x | Инструмент сборки frontend |
| **Runtime Frontend** | Node.js | 20+ | Окружение для сборки frontend |
| **Веб-сервер** | Nginx | 1.27-alpine | Reverse proxy, статические файлы |
| **База данных** | PostgreSQL | 16-alpine | Хранение данных |
| **Админ БД** | pgAdmin 4 | 8.2 | Веб-интерфейс управления БД |
| **Container Registry** | Docker Registry | 2 | Приватное хранилище образов |
| **Автообновление** | Watchtower (форк nickfedor) | latest | Жизненный цикл контейнеров (совместим с Docker 29) |
| **Оркестрация** | Docker Compose | v2+ | Управление сервисами |
| **ОС** | Ubuntu Server | 22.04 LTS | Операционная система VPS |

---

### 📋 Требования

#### Локальная машина (Windows 11)
- **Cursor IDE** с расширением Remote-SSH
- **SSH клиент** (встроен в Windows 10/11)
- **Git** (для клонирования репозитория)

#### VPS сервер
- **Ubuntu 22.04 LTS** (рекомендуется 2 CPU, 2 GB RAM, 10 GB SSD)
- **Публичный IPv4 адрес**
- **Доступ root** (или пользователь с sudo)
- **Открытые порты**: 22 (SSH), 80 (HTTP), 5000 (Registry), 5050 (pgAdmin)
- **Node.js 20+** и **npm** (для сборки frontend)

---

### 🚀 Быстрый старт

#### 1. Клонирование репозитория

```bash
git clone https://github.com/ergon73/order-processing-vps-infra.git
cd order-processing-vps-infra
```

#### 2. Настройка окружения

```bash
cp .env.example .env
nano .env
```

Установите сильные пароли (минимум 12 символов):
```env
POSTGRES_PASSWORD=ваш_сильный_пароль
PGADMIN_PASSWORD=другой_сильный_пароль
```

#### 3. Создание пользователя Registry

```bash
cd registry
chmod +x create-user.sh
./create-user.sh admin "ВашПарольДляRegistry"
cd ..
```

#### 4. Сборка frontend

```bash
cd frontend
npm ci
npm run build
cd ..
```

#### 5. Запуск сервисов

```bash
docker compose up -d --build
```

#### 6. Проверка развертывания

```bash
docker compose ps  # Все контейнеры должны быть в статусе "Up"
```

**Доступ к сервисам**:
- **Frontend**: `http://<VPS_IP>/`
- **Swagger UI**: `http://<VPS_IP>/api/docs`
- **API**: `http://<VPS_IP>/api/`
- **pgAdmin**: `http://<VPS_IP>:5050`
- **Registry**: `http://<VPS_IP>:5000/v2/`

---

### 🔌 Сервисы и порты

| Сервис | Имя контейнера | Внутренний порт | Внешний порт | Доступ |
|--------|---------------|-----------------|--------------|--------|
| **Nginx** | `nginx` | 80 | 80 | Публичный |
| **FastAPI Backend** | `backend` | 8000 | ❌ Не открыт | Только внутренний (через Nginx /api/) |
| **PostgreSQL** | `postgres` | 5432 | ❌ Не открыт | Только внутренний |
| **pgAdmin** | `pgadmin` | 80 | 5050 | Публичный (dev) |
| **Registry** | `registry` | 5000 | 5000 | Публичный (с аутентификацией) |
| **Watchtower** | `watchtower` | - | - | Фоновый |

⚠️ **Безопасность в продакшене**: В продакшен окружениях ограничьте доступ к портам `5050` и `5000` только через VPN/доверенные IP.

---

### ⚙️ Конфигурация

#### Переменные окружения (.env)

```env
# Конфигурация PostgreSQL
POSTGRES_DB=app_db          # Имя базы данных
POSTGRES_USER=app_user      # Пользователь БД
POSTGRES_PASSWORD=***       # Пароль БД (ИЗМЕНИТЕ!)

# Конфигурация pgAdmin
PGADMIN_EMAIL=admin@example.com    # Email для входа в pgAdmin
PGADMIN_PASSWORD=***               # Пароль pgAdmin (ИЗМЕНИТЕ!)
```

#### Сервисы Docker Compose

Редактируйте `docker-compose.yml` для настройки:
- **Лимиты ресурсов**: Добавьте `deploy.resources.limits` для CPU/памяти
- **Сети**: Измените конфигурации сетей
- **Тома**: Измените пути монтирования томов
- **Окружение**: Добавьте переменные окружения для сервисов

#### Конфигурация Nginx

- **Основной конфиг**: `nginx/nginx.conf`
- **Блоки серверов**: `nginx/conf.d/default.conf`
- **Статические файлы**: `nginx/html/`

Пример: Добавление HTTPS (требуются SSL сертификаты):
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... остальная конфигурация
}
```

---

### 📦 Развертывание

#### Первоначальное развертывание

```bash
# На VPS
mkdir -p /root/order-processing-vps-infra
cd /root/order-processing-vps-infra

# Копирование файлов или клонирование репозитория
git clone <repo_url> .

# Настройка
cp .env.example .env
nano .env  # Заполните пароли
cd registry && ./create-user.sh admin "пароль" && cd ..

# Запуск
docker compose up -d
```

#### Обновление сервисов

```bash
docker compose pull          # Скачать последние образы
docker compose up -d         # Пересоздать обновленные контейнеры
```

Или позвольте Watchtower делать это автоматически (каждые 5 минут).

#### Резервное копирование БД

```bash
docker exec postgres pg_dump -U app_user app_db > backup.sql
```

#### Восстановление БД

```bash
cat backup.sql | docker exec -i postgres psql -U app_user app_db
```

---

### 🔐 Безопасность

#### Реализованные меры

✅ **PostgreSQL**: Без внешних портов, только внутренняя Docker сеть  
✅ **SSH**: Аутентификация по ключу, вход по паролю отключен  
✅ **Registry**: Аутентификация htpasswd  
✅ **Секреты**: Файл `.env` исключен из git  
✅ **Healthchecks**: Автоматический мониторинг сервисов  
✅ **Минимальные привилегии**: Контейнеры запускаются от non-root где возможно  

#### Рекомендации для продакшена

🔒 **Включите HTTPS**: Используйте Let's Encrypt для SSL сертификатов  
🔒 **Файрвол**: Ограничьте порты с помощью `ufw` или файрвола облачного провайдера  
🔒 **VPN/Bastion**: Скрывайте pgAdmin/Registry за VPN или SSH туннелем  
🔒 **Мониторинг**: Добавьте Prometheus + Grafana для метрик  
🔒 **Резервные копии**: Автоматические ежедневные бэкапы PostgreSQL  
🔒 **Управление секретами**: Используйте Docker Secrets или Vault  

---

### 🐛 Решение проблем

#### Контейнер перезапускается

```bash
# Проверьте логи
docker compose logs --tail=200 <имя_сервиса>

# Частые проблемы:
# - postgres: Неправильный POSTGRES_PASSWORD в .env
# - registry: Отсутствует файл auth/htpasswd
# - pgadmin: Неправильный PGADMIN_PASSWORD
```

#### Ошибка аутентификации Registry

```bash
# Проверьте существование файла htpasswd
ls -l registry/auth/htpasswd

# Пересоздайте пользователя
cd registry
rm auth/htpasswd
./create-user.sh admin "новый_пароль"
docker compose restart registry
```

#### pgAdmin не подключается к PostgreSQL

- **Host** должен быть `postgres` (имя контейнера!), НЕ `localhost` или `127.0.0.1`
- **Port** это `5432`
- Проверьте, что оба контейнера в одной сети:
  ```bash
  docker network inspect order-processing-vps-infra_backend_network
  ```

#### Нет места на диске

```bash
df -h                    # Проверка использования диска
docker system df         # Использование Docker
docker system prune -a   # Очистка неиспользуемых ресурсов
```

#### Совместимость Watchtower

**Примечание**: Этот проект использует форк `nickfedor/watchtower` вместо оригинального `containrrr/watchtower`, потому что:
- Оригинальный Watchtower был архивирован (17 дек 2025) и несовместим с Docker 29
- Форк поддерживает Docker API 1.44+, требуемый для Docker 29
- Вся функциональность остается той же (автообновления каждые 5 минут)

Если видите ошибки версии API с Watchtower, убедитесь, что используете форк:
```bash
# Проверьте текущий образ
docker compose config | grep watchtower

# Должно показать: image: nickfedor/watchtower:latest
```

---

### 📁 Структура проекта

```
order-processing-vps-infra/
├── docker-compose.yml          # Основной файл оркестрации
├── .env.example                # Шаблон переменных окружения
├── .env                        # Фактические секреты (не в git)
├── .gitignore                  # Исключения для git
├── README.md                   # Этот файл (основная документация)
├── nginx/
│   ├── nginx.conf              # Основной конфиг Nginx
│   ├── conf.d/
│   │   └── default.conf        # Конфигурация блоков (API proxy + статика)
│   └── ssl/                    # SSL сертификаты (не в git)
├── backend/                    # FastAPI backend приложение
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # Точка входа FastAPI приложения
│   ├── core/
│   │   └── database.py         # Подключение к БД
│   ├── models/                 # SQLAlchemy модели
│   │   ├── admin_settings.py
│   │   ├── applications.py
│   │   └── behavior_metrics.py
│   └── routes/                 # API маршруты
│       ├── admin_settings.py
│       └── applications.py
├── frontend/                   # Webpack frontend приложение
│   ├── package.json
│   ├── webpack.config.js
│   ├── src/
│   │   ├── index.html          # HTML шаблон
│   │   ├── index.js            # Логика приложения
│   │   └── styles.css          # "Элитный" стиль CSS
│   └── dist/                   # Результат сборки (генерируется, не в git)
│       ├── index.html
│       ├── main.*.css          # Извлеченный CSS
│       └── main.*.js           # Собранный JavaScript
└── registry/
    ├── create-user.sh          # Скрипт создания пользователя Registry
    └── auth/
        └── htpasswd            # Учетные данные Registry (не в git)
```

---

### 🤝 Вклад в проект

Вклад приветствуется! Пожалуйста, следуйте этим шагам:

1. Сделайте форк репозитория
2. Создайте ветку для функции: `git checkout -b feature/amazing-feature`
3. Закоммитьте изменения: `git commit -m 'Добавить amazing feature'`
4. Отправьте в ветку: `git push origin feature/amazing-feature`
5. Откройте Pull Request

**Стиль кода**:
- Используйте shellcheck для bash скриптов
- Валидируйте YAML с yamllint
- Тестируйте локально перед PR

---

### 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

---

### 👤 Автор

**Georgy**  
Студент курса Vibe-Coding  
📧 Контакт: [GitHub Profile](https://github.com/ergon73)

---

### 🙏 Благодарности

- **Курс**: [ZeroCoder - Vibe-Coding](https://zerocoder.ru)
- **Преподаватель**: Модуль 8 - Автоматизация бизнес-процессов
- **Инструменты**: Docker, Nginx, PostgreSQL, Watchtower

---

### 📊 Статус проекта

✅ **Этап 1**: Настройка инфраструктуры (nginx, postgres, pgadmin, registry, watchtower)  
✅ **Этап 2**: Развертывание backend приложения (FastAPI + PostgreSQL + SQLAlchemy)  
✅ **Этап 3**: Интеграция frontend (Webpack + Vanilla JS, "элитный" дизайн)

**Текущая версия**: Часть 2 - Full-stack приложение с backend и frontend

**Статус**: ✅ **Готово к продакшену** - Все компоненты функциональны, протестированы и развернуты

---

**⭐ Если этот проект помог вам, пожалуйста, поставьте звезду!**
