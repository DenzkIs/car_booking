from django.apps import AppConfig


class RisolaUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risola_users'

    def ready(self):
        import risola_users.signals
