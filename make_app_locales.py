import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.transutils import get_apps_for_translation


def delete_symlink_if_broken(path):
    try:
        if not os.path.exists(os.readlink(path)):
            os.remove(path)
    except (FileNotFoundError, OSError):
        pass


class Command(BaseCommand):
    """
    creates all locale directories as symlinks to the "language files" volume
    """

    def handle(self, **options):
        with open(f'{settings.BASE_DIR}/app_requirements/{settings.HOSTNAME}.txt') as f:
            apps = get_apps_for_translation(f)

        language_volume = getattr(settings, 'LANGUAGE_VOLUME', 'language_files')

        self.stdout.write(f"Creating app locales for {len(apps)} apps")
        for app in apps:
            path = app['locale_dir']
            delete_symlink_if_broken(path)

            destination = Path(f'{settings.BASE_DIR}/{language_volume}/{app["app_name"]}/locale')

            # create the symlink
            if not os.path.exists(destination):
                os.makedirs(destination)
            if not os.path.exists(path):
                path.symlink_to(destination)

            # create the language directories
            for lang in app['languages']:
                if not os.path.exists(f'{destination}/{lang}'):
                    os.makedirs(f'{destination}/{lang}')
