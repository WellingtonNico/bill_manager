from django.apps import AppConfig


class RelatoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relatories'

    def ready(self) -> None:
        super().ready()
        from . import signals