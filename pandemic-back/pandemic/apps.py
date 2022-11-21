import os

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'pandemic'
    verbose_name = "My Application"

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from pandemic.game import play_game
            play_game()
