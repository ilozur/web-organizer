from django.contrib.auth.models import User
from django.test import TestCase, Client


# Create your tests here.

class TestMainPage ( TestCase ):

    def setUp( self ):
        u = User(username='testuser', is_active=1)
        u.set_password('password123')
        self.c = Client()

    def test_redirect(self):
        self.c.get('/')
        response = self.c.post('/', {
            'user': 'test',
            'pass': '123454321'
        })
        self.assertRedirects(response, '/')

    def test_non_auth_template(self):
        c = Client()
        response = c.get('/')
        self.assertEqual ( response.status_code, 200 )
        self.assertTemplateUsed(response, 'main/index.html')

    def test_auth_html ( self ):
        self.c.login (username='testuser', password = 'password123')
        response = self.c.get('/')
        self.assertContains ( response, 'Добрый день' )
        self.assertContains ( response, 'Последние заметки' )
        self.assertContains ( response, 'Ближайшие события календаря' )