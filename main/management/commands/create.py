from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
from notes.models import Notes
from calendars.models import Event


class Command ( BaseCommand ):
    args = "there's no args"

    Lopsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco\
                 laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate \
                 velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
                 sunt in culpa qui officia deserunt mollit anim id est laborum."

    def us ( self ):
        return User.objects.all ()

    def notes ( self ):
        return Notes.objects.all ()

    def events ( self ):
        return Event.objects.all ()

    def handle ( self, *args, **options ):
        self.deleteall ()
        for i in range ( 0, 50 ):
            self.create_user ( username='test_user_{}'.format ( i ), password=" ", email=None )
            for j in self.us ():
                self.create_note ( text=self.Lopsum, name="Lorem Ipsum", user=j, time=datetime.datetime.now () )
                self.create_calendar ( date="2108-01-01", content=self.Lopsum, user=j )

    def create_user ( self, username, password, email ):
        u = User.objects.create_user ( username, email, password )
        u.save ()

    def create_note ( self, text, name, user, time ):
        n = Notes ( data=text, user=user, added_time=time, name=name )
        n.save ()

    def create_calendar ( self, date, content, user ):
        e = Event ( user=user, date=date, description=content, time=datetime.time().now(), is_public=True )
        e.save ()

    def deleteall ( self ):
        for e in self.events():
            e.delete ()
            print('event deleted')
        for n in self.notes():
            n.delete ()
            print('note deleted')
        for i in self.us ():
            i.delete ()
            print('user deleted')
