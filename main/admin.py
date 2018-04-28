from django.contrib import admin
import main.management.commands.generate_notes as gn
import main.management.commands.generate_events as ge
import main.management.commands.generate_todo as gt
import main.management.commands.generate_users as gu
import main.management.commands.createuser as cu


# Register your models here.
@admin
def index():
    pass

def creation(argument, number):
    if argument == 'n' or argument == 'N':
        gn.Command.generate_notes(number)
    elif argument == 'e' or argument == 'E':
        ge.Command.generate_events(number)
    elif argument == 't' or argument== 'T':
        gt.Command.generate_todo(number)
    elif argument == 'u' or argument == 'U':
        gu.Command.generate_users(number)


def user_create(nickname, password, lang):
    cu.Command.create_user(nickname,password,lang)