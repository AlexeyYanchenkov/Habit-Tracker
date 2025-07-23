from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from habits.models import Habit
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import localtime
import json

@receiver(post_save, sender=Habit)
def create_periodic_task_for_habit(sender, instance, created, **kwargs):
    if not instance.reminder_time or not instance.periodicity:
        return

    # Преобразуем время в локальное
    local_time = localtime().replace(hour=instance.reminder_time.hour, minute=instance.reminder_time.minute)

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=str(local_time.minute),
        hour=str(local_time.hour),
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    PeriodicTask.objects.update_or_create(
        name=f"habit-{instance.id}",
        defaults={
            'crontab': schedule,
            'task': 'habits.tasks.send_habit_reminder',
            'args': json.dumps([instance.id]),
        }
    )

@receiver(post_delete, sender=Habit)
def delete_periodic_task_for_habit(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f"habit-{instance.id}").delete()