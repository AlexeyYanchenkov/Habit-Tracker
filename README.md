# Habit-Tracker

Проект трекера привычек на Django с REST API и автоматическим CI/CD.

---

## Быстрый старт (локально)

### Предварительные требования

- Python 3.10.12
- Docker и Docker Compose 
- PostgreSQL 
- Git

### Клонирование репозитория

git clone https://github.com/yourusername/Habit-Tracker.git
cd Habit-Tracker
Настройка виртуального окружения и установка зависимостей

python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
Настройка переменных окружения
Создайте файл .env в корне проекта, используя .env.sample как шаблон, и заполните необходимые значения:

env

SECRET_KEY=your_secret_key
DEBUG=False
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
Запуск локальной базы данных (PostgreSQL)
Если у вас нет PostgreSQL, вы можете запустить его через Docker:

docker run --name habit_tracker_postgres -e POSTGRES_USER=your_db_user -e POSTGRES_PASSWORD=your_db_password -e POSTGRES_DB=your_db_name -p 5432:5432 -d postgres:15

Применение миграций и запуск сервера:

python manage.py migrate
python manage.py runserver
Теперь проект доступен по адресу http://127.0.0.1:8000

Запуск проекта одной командой (через Docker Compose)
Если установлен Docker и Docker Compose:

docker-compose up --build
Это запустит все сервисы (включая БД) и сервер Django.

CI/CD и автоматический деплой
В проекте настроен GitHub Actions workflow для автоматического тестирования, сборки и деплоя на удалённый сервер при пуше в ветку main.

Основные моменты настройки
Secrets GitHub репозитория

Перейдите в Settings → Secrets and variables → Actions и добавьте:

SECRET_KEY — секрет Django

DEBUG — False

DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT — параметры БД для тестов

TELEGRAM_BOT_TOKEN — токен Telegram-бота

SERVER_HOST — IP или домен сервера

SERVER_USER — пользователь SSH

SERVER_SSH_KEY — приватный SSH ключ для доступа к серверу

Workflow GitHub Actions

Файл .github/workflows/deploy.yml:

Запускает тесты с поднятием PostgreSQL сервиса

Собирает Docker-образы

Через SSH подключается к серверу и выполняет:

cd /home/<SERVER_USER>/Habit-Tracker
docker-compose pull
docker-compose up -d --build



Деплой на сервер вручную (если нужно)

git clone https://github.com/yourusername/Habit-Tracker.git
cd Habit-Tracker
docker-compose up -d --build
