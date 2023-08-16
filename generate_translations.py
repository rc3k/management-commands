import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    A wrapper around a series of sequential management commands
    does full generate of translations
    """
    def handle(self, **options):

        # create app locale holders (symlinks to the language file volume)
        call_command('make_app_locales')

        # make messages for all apps
        call_command('make_app_messages')

        # auto-generate placeholder messages
        call_command('make_placeholder_messages')

        # message compilation (core Django)
        os.chdir(settings.BASE_DIR)
        call_command('compilemessages')
