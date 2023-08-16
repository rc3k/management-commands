import subprocess
import re

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, **options):
        """
        "gracefully reload" all gunicorn process for the current app
        see https://docs.gunicorn.org/en/latest/faq.html
        """

        ps1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
        ps2 = subprocess.Popen(['grep', 'gunicorn'], stdin=ps1.stdout, stdout=subprocess.PIPE)
        ps3 = subprocess.Popen(['grep', f'acn-{settings.HOSTNAME}'], stdin=ps2.stdout, stdout=subprocess.PIPE)

        processes = [re.split('\s+', p) for p in ps3.communicate()[0].decode().split('\n')]
        pids = [p[1] for p in processes if len(p) > 1]
        for pid in pids:
            subprocess.run(['kill', '-HUP', pid])
