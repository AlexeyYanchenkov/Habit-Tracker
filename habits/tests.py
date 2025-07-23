from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import timedelta, localtime
from datetime import time
from habits.models import Habit
from django.contrib.auth import get_user_model
from unittest.mock import patch
from habits.tasks import send_habit_reminders

User = get_user_model()


class HabitPaginationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

        for i in range(6):
            Habit.objects.create(
                user=self.user1,
                action=f"Action {i}",
                is_public=False,
                is_pleasant=True,
                time=time(12, 0),
                execution_time=timedelta(seconds=60)
            )

        self.public_habit = Habit.objects.create(
            user=self.user2,
            action="Public Habit",
            is_public=True,
            is_pleasant=True,
            time=time(12, 0),
            execution_time=timedelta(seconds=60)
        )

    def test_paginated_habit_list_page_1(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/habits/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 6)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        actions = [habit['action'] for habit in response.data['results']]
        for i in range(5):
            self.assertIn(f"Action {i}", actions)

    def test_paginated_habit_list_page_2(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/habits/?page=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 6)

        action = response.data['results'][0]['action']
        self.assertEqual(action, "Action 5")

    def test_public_habit_visible_to_others(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/public-habits/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], 'Public Habit')

    def test_user_does_not_see_others_private_habits(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/habits/')

        actions = [habit['action'] for habit in response.data['results']]
        self.assertNotIn('Public Habit', actions)

    def test_unauthorized_access_is_denied(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_delete_someone_elses_public_habit(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/habits/{self.public_habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_habit(self):
        self.client.force_authenticate(user=self.user1)
        habit = Habit.objects.filter(user=self.user1).first()
        response = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('habits.tasks.send_telegram_message.delay')
    def test_send_habit_reminders_task(self, mock_send):
        """
        Проверяем, что задача send_habit_reminders находит привычки и отправляет сообщения
        """
        # Добавим telegram_chat_id
        self.user1.telegram_chat_id = '123456789'
        self.user1.save()

        now = localtime().replace(second=0, microsecond=0)
        Habit.objects.create(
            user=self.user1,
            action='Утренняя зарядка',
            reminder_time=now.time(),
            is_public=False,
            is_pleasant=False,
            time=now.time(),
            execution_time=timedelta(minutes=1)
        )

        send_habit_reminders()

        mock_send.assert_called_once_with(
            self.user1.telegram_chat_id,
            "Напоминание: пора делать привычку 'Утренняя зарядка'!"
        )
