# Запуск Celery
celery -A config worker --loglevel=info


# Запуск beat-планировщика
celery -A config beat --loglevel=info


# Запуск Django-сервера
python manage.py runserver

