import os

from django.core.management.base import BaseCommand

from pre_commit.commands.install_uninstall import install as pre_commit_install
from pre_commit.store import Store

from devtools.requirements import RequirementsParser
from devtools.gittools import GitTools


class Command(BaseCommand):
    help = "Install pre-commit hooks for Anthesis apps"

    def add_arguments(self, parser):
        parser.add_argument(
            "-a", "--app", type=str, help="The label/slug of an Anthesis App"
        )

    def handle(self, **options):
        git = GitTools()
        dev = RequirementsParser(git).get_dev_environment()
        app_label = options.get('app', None)
        for app in dev['apps']:
            if app_label and app_label != app['app_label']:
                continue
            yaml_file = os.path.join(app['location'], '.pre-commit-config.yaml')

            #  A .pre-commit-config.yaml file must exist within the app
            if os.path.exists(yaml_file):
                self.stdout.write(f"{app['app_name']}")
                pre_commit_install(
                    '.pre-commit-config.yaml',
                    Store(),
                    hook_types=['commit-msg', 'pre-push'],
                    git_dir=os.path.join(app['location'], '.git')
                )
            else:
                self.stderr.write(f"A .pre-commit-config.yaml file does not exist for {app['app_name']}")
