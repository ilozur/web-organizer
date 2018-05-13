from django.contrib.auth.models import User
from django.test import TestCase, Client
from notes.models import *
from datetime import *
from todo.models import *

class TestMainPage(TestCase):

    def setUp(self):
        global u
        u = User(username='testuser', is_active=1,
                 first_name='Vasya', last_name='Pupkin')
        u.set_password('pass')
        u.save()
        self.c = Client()

    def test_post_redirect(self):
        response = self.c.post('/', {'this':'is', 'dummy':'context'})
        self.assertRedirects(response, '/')

    def test_index_non_auth(self):
        
        response = self.c.get('/')
        # check status code
        self.assertEqual(response.status_code, 200)

        # check template
        self.assertTemplateUsed(response, 'main/index.html')

        # check html
        self.assertContains(response, 'Добро пожаловать')
        self.assertContains(response, "Enter your password")

    def test_index_with_auth(self):
        self.c.login(username='testuser', password='pass')
        response = self.c.get('/')

        # check status code
        self.assertEqual(response.status_code, 200)

        # check template
        self.assertTemplateUsed(response, 'main/home.html')

        # check context. Assuming db is empty.
        # TODO: fill db and check
        self.assertEqual(response.context['last_notes_count'], 0)

        # check html
        self.assertContains(response, 'Добрый день')
        self.assertContains(response, 'Последние заметки')
        self.assertContains(response, 'Ближайшие события календаря')

    def test_Notes(self):
        self.c.login(username="testuser", password="pass")
        response = self.c.get('/notes')

        # check status code
        self.assertEqual(response.status_code, 200)

        # check template
        self.assertTemplateUsed(response, 'notes/index.html')

        # check the adding process
        all_notes = Notes.objects.all()
        context = {'data_part':'test value',
                   'datetime':datetime.datetime.now(),
                   'name':'test note',
                   'id':'{}'.format(len(all_notes) + 1)}
        response = self.c.post('/notes/add', context)

        self.assertEqual(response.status_code, 200)

        response = self.c.post('/notes/add', context)

        self.assertEqual(response.result, 100)

        response = self.c.post('/notes/add', context)

        self.assertEqual(response.result, 100)

        # check the showing process
        response = self.c.get('/notes/get_note_data')
        self.assertEqual(response.result, 100)

    def test_Todo(self):
        self.c.login(username="testuser", password="pass")
        response = self.c.get('/todo')

        # check status code
        self.assertEqual(response.status_code, 200)

        # check template
        self.assertTemplateUsed(response, 'todo/index.html')

        # check the adding process
        all_todos = Todos.objects.all()
        context = {'priority':5,
            'datetime':datetime.datetime.now(),
            'title':'test todo',
            'id':'{}'.format(len(all_todos) + 1)}

        response = self.c.post('/todo/add', context)

        self.assertEqual(response.result, "Success")

        # check the showing process
        response = self.c.get('/todo/show_todo')
        self.assertEqual(response.result, "Success")