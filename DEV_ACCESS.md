# Доступ к dev-сервисам (pgAdmin и Registry)

## Как включить pgAdmin для администрирования PostgreSQL

По умолчанию pgAdmin и Registry **отключены** в продакшене (требование задания).

Для доступа к pgAdmin (управление БД):

```bash
# Включить pgAdmin и Registry
docker compose --profile dev up -d pgadmin registry

# Проверить статус
docker compose ps

# Открыть pgAdmin в браузере
# http://194.67.205.158:5050
```

## Как отключить dev-сервисы

```bash
# Остановить и удалить контейнеры
docker compose --profile dev down pgadmin registry
```

## Важно

- **В продакшене**: pgAdmin и Registry отключены (безопасность)
- **Для администрирования**: включайте через `--profile dev`
- **После работы**: отключайте обратно для безопасности

## Альтернативный способ доступа к PostgreSQL

Если не хотите использовать pgAdmin, можно подключиться напрямую через Docker:

```bash
# Подключиться к PostgreSQL через Docker exec
docker exec -it postgres psql -U app_user -d app_db

# Или через docker compose
docker compose exec postgres psql -U app_user -d app_db
```
