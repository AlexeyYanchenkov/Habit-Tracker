from unittest.mock import patch
from django.test import TestCase
from users.tasks import send_telegram_message


class UsersTasksTests(TestCase):

    @patch('users.tasks.requests.post')
    def test_send_telegram_message(self, mock_post):
        chat_id = '123456789'
        message = 'Тестовое сообщение'

        # Имитация успешного ответа от Telegram API
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'ok': True}

        # Запускаем задачу напрямую (не delay)
        send_telegram_message(chat_id, message)

        # Проверяем, что был сделан HTTP-запрос с нужными параметрами
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert 'sendMessage' in args[0]
        assert kwargs['data']['chat_id'] == chat_id
        assert kwargs['data']['text'] == message
