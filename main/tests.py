from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestMainPage(TestCase):

    def setUp(self):
        u = User(username='testuser', is_active=1,
                 first_name='Vasya', last_name='Pupkin')
        u.set_password('pass')
        u.save()
        self.c = Client()

    def test_redirect(self):
        response = self.c.post('/',
                          {'user': 'test',
                           'pass': 'ppp'})

        self.assertRedirects(response, '/')

    def test_non_auth_template(self):
        response = self.c.get('/')
        self.assertTemplateUsed(response,
                                'main/index.html')
        self.assertEqual(response.status_code, 200)

    def test_auth_template(self):
        self.c.login(username='testuser', password='pass')
        response = self.c.get('/')
        self.assertTemplateUsed(response,
                                'main/home.html')
        self.assertEqual(response.status_code, 200)

    def test_non_auth_html(self):
        response = self.c.get('/')
        self.assertContains(response, 'Добро пожаловать')
        self.assertContains(response, "Enter your password")

    def test_auth_html(self):
        self.c.login(username='testuser', password='pass')
        response = self.c.get('/')
        self.assertContains(response, 'Добрый день')
        self.assertContains(response, 'Последние заметки')
        self.assertContains(response, 'Ближайшие события календаря')

    def test_auth_context(self):
        self.c.login(username='testuser', password='pass')
        response = self.c.get('/')
        self.assertEqual(response.context['last_notes_count'], 0)