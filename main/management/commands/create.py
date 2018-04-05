from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = "there's no args"
    none = None
    users = []
    Lopsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco\
                 laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate \
                 velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
                 sunt in culpa qui officia deserunt mollit anim id est laborum."
    def creation( self ):
        for i in range (0, 50):
            users.append(create_user(username = 'test_user_{}'.format(i), password = " ", email = None))
            for j in range(0, i):
                create_note(text=Lopsum, name = "Lorem Ipsum", user = )

    def create_user( self, username, password, email ):
        u = User.objects.create_user(username, email, password)
        u.save()


    def create_note( self, text, name, user ):
        pass