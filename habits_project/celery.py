import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habits_project.settings')

app = Celery('habits_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-habit-reminders-every-minute': {
        'task': 'habits.tasks.send_habit_reminders',
        'schedule': crontab(),  # запускается каждую минуту
    },
}