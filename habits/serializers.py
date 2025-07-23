from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    execution_time = serializers.DurationField()  # DRF умеет работать с DurationField

    class Meta:
        model = Habit
        fields = [
            'id', 'place', 'time', 'action', 'is_pleasant', 'related_habit',
            'reward', 'periodicity', 'execution_time', 'is_public', 'reminder_time'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        # 1. Приятная привычка не может иметь вознаграждение или связанную привычку
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError("Приятная привычка не может иметь вознаграждение.")
            if data.get('related_habit'):
                raise serializers.ValidationError("Приятная привычка не может иметь связанную привычку.")
        # 2. Нельзя одновременно указать и вознаграждение, и связанную привычку
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Нельзя одновременно указать и вознаграждение, и связанную привычку.")
        # 3. Периодичность не должна быть больше 7
        if data.get('periodicity', 1) > 7:
            raise serializers.ValidationError("Периодичность не может быть больше 7 дней.")
        # 4. Время выполнения не больше 120 секунд
        execution_time = data.get('execution_time')
        if execution_time and execution_time.total_seconds() > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")
        return data