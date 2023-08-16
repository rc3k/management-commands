import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from polib import pofile

from core.transutils import get_apps_for_translation


class Command(BaseCommand):
    """
    make all django.po files for the placeholder language across the whole project
    then, replace all message string (mgstr) with a placeholder (the msgid wrapped in some garbage text)
    """

    def handle(self, **options):
        try:
            if not settings.PLACEHOLDER_LANGUAGE:
                raise Exception(_("PLACEHOLDER_LANGUAGE does not exist"))

            self.stdout.write("Auto-generating placeholder messages")

            filenames = ['django.po', 'djangojs.po']
            with open(f'{settings.BASE_DIR}/app_requirements/{settings.HOSTNAME}.txt') as f:
                apps = get_apps_for_translation(f)

            locale_dirs = [app['locale_dir'] for app in apps] + list(settings.LOCALE_PATHS)
            for dir in locale_dirs:
                for filename in filenames:
                    po_file_path = os.path.join(dir, settings.PLACEHOLDER_LANGUAGE, 'LC_MESSAGES', filename)
                    if not os.path.exists(po_file_path):
                        continue
                    po_file = pofile(
                        po_file_path
                    )
                    for entry in po_file:
                        prefix = ''
                        suffix = ''
                        if entry.msgid.startswith('\n'):
                            prefix = '\n'
                        if entry.msgid.endswith('\n'):
                            suffix = '\n'
                        entry.msgstr = f"{prefix}**[[[{entry.msgid}]]]**{suffix}"
                    po_file.save()
        except Exception as e:
            print(f"An error has occurred creating the placeholder language: {e}")
            raise
