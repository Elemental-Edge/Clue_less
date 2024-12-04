from django.apps import AppConfig


class GamemanagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Backend.GameManagement"

    def ready(self):
        print("instantiating Singleton")
        from Backend.GameManagement.singleton import Singleton
        self.single = Singleton()

    def get_singleton(self):
        print("get Singleton")
        return self.single
