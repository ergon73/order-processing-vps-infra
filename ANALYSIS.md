# Анализ инструкций - Неувязки и противоречия

## 🔴 Критические неувязки

### 1. **Монтирование статики Frontend в Nginx**

**Проблема:**
- `docker-compose.yml` (строка 12): `./nginx/html:/usr/share/nginx/html:ro`
- `genai-readme-2.md` (строка 577): `./frontend/dist:/usr/share/nginx/html:ro`
- `.cursorrules` (строка 263): `./frontend/dist:/usr/share/nginx/html:ro`

**Текущее состояние:**
- В проекте существует `nginx/html/` с заглушкой `index.html`
- Директории `frontend/` нет

**Решение:**
- При создании frontend нужно изменить монтирование в `docker-compose.yml`
- Заменить `./nginx/html` на `./frontend/dist`

---

### 2. **Имя пользователя PostgreSQL по умолчанию**

**Проблема:**
- `docker-compose.yml` (строка 30): `POSTGRES_USER:-app_user` (default: `app_user`)
- `.env` (из вывода): `POSTGRES_USER=app_user`
- `genai-readme-2.md` (строка 325): `POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")` (default: `admin`)

**Последствия:**
- Если backend не получит `POSTGRES_USER` из окружения, будет использовать `admin`
- Но в PostgreSQL создан пользователь `app_user`

**Решение:**
- В `backend/core/database.py` изменить default на `"app_user"` или
- Убедиться, что переменная окружения передается в backend из docker-compose.yml

---

## ⚠️ Потенциальные проблемы

### 3. **Упоминание `/services/` как альтернативного endpoint**

**Наблюдение:**
- `human-readme-2.md` (строка 14): упоминает `/api/services/` как альтернативу
- Во всех остальных документах используется только `/api/admin-settings/`

**Решение:**
- Использовать только `/admin-settings/` согласно `.cursorrules` и `genai-readme-2.md`

---

### 4. **Структура маршрутов в Backend**

**В genai-readme-2.md:**
- Router prefix: `/admin-settings` (строка 356)
- Эндпоинты: `POST /`, `GET /latest`, `GET /`
- Результат: `/admin-settings/`, `/admin-settings/latest`, `/admin-settings/`

**В .cursorrules:**
- Структура совпадает (строки 68-75)

**Статус:** ✅ Согласовано

---

### 5. **Healthcheck для PostgreSQL**

**Проблема:**
- `docker-compose.yml` (строка 39): `pg_isready -U ${POSTGRES_USER:-app_user}`
- Это правильно, но нужно проверить, что backend использует тот же пользователь

**Статус:** ✅ Потенциально OK, но нужно проверить

---

## 📝 Рекомендации по устранению

### Приоритет 1 (Критично):
1. **Изменить монтирование в docker-compose.yml:**
   ```yaml
   nginx:
     volumes:
       - ./frontend/dist:/usr/share/nginx/html:ro  # вместо ./nginx/html
   ```

### Приоритет 2 (Важно):
2. **Синхронизировать POSTGRES_USER в backend:**
   ```python
   # backend/core/database.py
   POSTGRES_USER = os.getenv("POSTGRES_USER", "app_user")  # вместо "admin"
   ```

### Приоритет 3 (Проверка):
3. **Убедиться, что в docker-compose.yml backend получает переменные окружения:**
   ```yaml
   backend:
     environment:
       POSTGRES_USER: ${POSTGRES_USER}
       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
       POSTGRES_DB: ${POSTGRES_DB}
       POSTGRES_HOST: postgres
   ```

---

## ✅ Что согласовано правильно

1. ✅ Структура маршрутов `/admin-settings/` и `/applications/`
2. ✅ Использование trailing slashes в API endpoints
3. ✅ Структура моделей БД (AdminSettings, Applications, BehaviorMetrics)
4. ✅ Использование MiniCssExtractPlugin для CSS
5. ✅ Nginx location order (статичные файлы → API proxy → SPA fallback)
6. ✅ Использование `POSTGRES_HOST=postgres` (не localhost)
