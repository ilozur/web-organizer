from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestMainPage(TestCase):

    def setUp(self):
        u = User(username='testuser', is_active=1,
                 first_name='Vasya', last_name='Pupkin')
        u.set_password('pass')
        u.save()
        self.c = Client()

    def test_post_redirect(self):
        response = self.c.post('/', {'this': 'is', 'dummy': 'context'})
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
    
    def test_TodoAdd(self):
        # check the adding process
        all_todos = Todos.objects.all()
        context = {
            'priority':5,
            'datetime':datetime.datetime.now(),
            'title':'test todo',
            'id':'{}'.format(len(all_todos) + 1)}


        response = self.c.post('/todo/add', context)
        self.assertEqual(response.context['result'], 302)
    
    def test_TodoHTML(self):
        self.c.login(username="testuser", password="pass")
        response = self.c.get('/todo')
        self.assertTemplateUsed(response, 'todo/index.html')

    def test_ShowTodos(self):
        self.c.login(username="testuser", password="pass")
        response = self.c.get('/todos/get_todo_data')
        self.assertEqual(response.context['result'], 100)
        
    def test_TodoShow(self):
        response = self.c.get('/todos/get_todo_data')
        self.assertEqual(response.status_code, 200, 'SC {}!'.format(response.context['result']))
        
     def test_Todos(self):
        self.c.login(username="testuser", password="pass")
        response = self.c.get('/todos')

        self.assertEqual(response.status_code, 200)
        all_todos = Todos.objects.all()

        response = self.c.post('/todos/add', {
            'data_part':'test value',
            'datetime':datetime.datetime.now(),
            'name':"test todo' or 1=1 DROP DATABASE;--",
            'id':'{}'.format(len(all_todos) + 1)})

        self.assertEqual(response.context['result'], 100)

    
    
    
