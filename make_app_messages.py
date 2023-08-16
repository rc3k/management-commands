import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

import vinaigrette
from core.transutils import get_apps_for_translation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--applabel',
            type=str,
            help="A specifc app label"
        )
        parser.add_argument(
            '--locale',
            type=str,
            help="A specifc locale"
        )

    def handle(self, applabel=None, locale=None, **options):
        with open(f'{settings.BASE_DIR}/app_requirements/{settings.HOSTNAME}.txt') as f:
            apps = get_apps_for_translation(f)
        if applabel:
            apps = [app for app in apps if app['app_name'] == applabel]
        if not apps:
            self.stderr.write(f"No such app with label {applabel}")
        for app in apps:
            self.stdout.write(f"Making messages for app '{app['app_name']}'")
            os.chdir(app['location'])

            locales = app['languages']

            if locale:
                locales = [lo for lo in app['languages'] if lo == locale]
            for locale in locales:
                vinaigrette._REGISTRY = {}
                if hasattr(app['config'], 'register_model_translations'):
                    app['config'].register_model_translations()
                call_command('makemessages', '--symlinks', locale=[locale])
                call_command('makemessages', '--symlinks', domain='djangojs', extension=['js'], locale=[locale])
            call_command('makemessages', '--symlinks', locale=[settings.PLACEHOLDER_LANGUAGE])
            call_command('makemessages', '--symlinks', domain='djangojs', extension=['js'], locale=[settings.PLACEHOLDER_LANGUAGE])
