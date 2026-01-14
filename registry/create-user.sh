#!/bin/bash

# Скрипт для создания пользователя в Docker Registry (htpasswd)
# Использование: ./create-user.sh <username> <password>

set -e

if [ "$#" -ne 2 ]; then
    echo "Использование: $0 <username> <password>"
    echo "Пример: $0 admin MyStrongPassword123"
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"

# Проверка наличия docker
if ! command -v docker &> /dev/null; then
    echo "Ошибка: Docker не установлен"
    exit 1
fi

# Создание директории для auth если не существует
mkdir -p auth

# Проверка существования файла htpasswd
if [ -f "auth/htpasswd" ]; then
    echo "Файл auth/htpasswd уже существует."
    echo "Добавляем нового пользователя или обновляем существующего..."
    
    # Обновление или добавление пользователя
    docker run --rm --entrypoint htpasswd httpd:2 -Bbn "$USERNAME" "$PASSWORD" >> auth/htpasswd
else
    echo "Создаем новый файл auth/htpasswd..."
    
    # Создание нового файла htpasswd
    docker run --rm --entrypoint htpasswd httpd:2 -Bbn "$USERNAME" "$PASSWORD" > auth/htpasswd
fi

# Установка правильных прав доступа
chmod 644 auth/htpasswd

echo "✓ Пользователь '$USERNAME' успешно создан/обновлен в auth/htpasswd"
echo ""
echo "Для входа в registry используйте:"
echo "  docker login <VPS_IP>:5000"
echo "  Username: $USERNAME"
echo "  Password: ******"
echo ""
echo "Проверка доступа:"
echo "  curl -u $USERNAME:<password> http://<VPS_IP>:5000/v2/"
echo "  Ожидаемый результат: {}"
