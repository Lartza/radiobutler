from django.apps import AppConfig


class RadiovisConfig(AppConfig):
    name = 'radiovis'

    def ready(self):
        import radiovis.signals # noqa
