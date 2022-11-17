import os

from django.apps import AppConfig

from pandemic import controller


class MyAppConfig(AppConfig):
    name = 'pandemic'
    verbose_name = "My Application"

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            controller.start_game()

