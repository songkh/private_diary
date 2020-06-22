from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Diary

class LoggedInTestCase(TestCase):

    def setUp(self):

        self.password = 'pass76029865'

        self.test_user = get_user_model().objects.create_user(
            username='test3',
            email='test3@example.com',
            password=self.password
        )

        self.client.login(email=self.test_user.email, password=self.password)

class TestDiaryCreateView(LoggedInTestCase):

    def test_create_diary_success(self):
        params = {
            'title': 'テストタイトル',
            'content': '本文',
            'photo1': '',
            'photo2': '',
            'photo3': ''
        }

        response = self.client.post(reverse_lazy('diary:diary_create'), params)
        self.assertRedirects(response, reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(title='テストタイトル').count(), 1)