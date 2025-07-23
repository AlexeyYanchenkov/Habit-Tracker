from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta


User = get_user_model()


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место'
    )

    time = models.TimeField(
        verbose_name='Время выполнения'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True},
        verbose_name='Связанная приятная привычка'
    )

    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )

    execution_time = models.DurationField(
        verbose_name='Время на выполнение'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )

    reminder_time = models.TimeField(
        null=True,
        blank=True
    )  # время для напоминания

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указать и вознаграждение, и связанную привычку.")

        # 2. Время выполнения не больше 120 секунд
        if self.execution_time is not None and self.execution_time > timedelta(seconds=120):
            raise ValidationError("Execution time слишком большое")

        # 3. В связанные привычки можно выбирать только привычки с флагом is_pleasant=True
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        # 5. Периодичность не должна превышать 7 дней
        if self.periodicity > 7:
            raise ValidationError("Периодичность не может быть больше 7 дней.")

    def save(self, *args, **kwargs):
        self.clean()  # Принудительно вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} — {self.user.email}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']
