from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import localtime

from habits.models import Habit
from users.tasks import send_telegram_message

@shared_task
def send_habit_reminder(habit_id):
    """
    Отправка напоминания по конкретной привычке (вручную, по ID).
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        chat_id = user.telegram_chat_id

        if chat_id:
            message = f"Напоминание: пора выполнить привычку — {habit.action}!"
            send_telegram_message.delay(chat_id, message)
    except Habit.DoesNotExist:
        pass

@shared_task
def send_habit_reminders():
    """
    Основная задача: каждая минута проверяет все привычки и отправляет напоминания.
    """
    now = localtime().replace(second=0, microsecond=0)
    start = (now - timedelta(minutes=1)).time()
    end = (now + timedelta(minutes=1)).time()

    habits = Habit.objects.filter(reminder_time__gte=start, reminder_time__lte=end)

    print(f"[send_habit_reminders] Текущее время: {now.time()}, найдено привычек: {habits.count()}")

    for habit in habits:
        user = habit.user
        chat_id = user.telegram_chat_id
        if chat_id:
            message = f"Напоминание: пора делать привычку '{habit.action}'!"
            send_telegram_message.delay(chat_id, message)  # отправляем асинхронно через другую задачу
            print(f"Отправлено сообщение пользователю {user.email} с chat_id {chat_id}")
        else:
            print(f"У пользователя {user.email} нет telegram_chat_id, пропускаю.")
