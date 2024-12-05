from django.apps import AppConfig


class GamemanagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Backend.GameManagement"

    def ready(self):
        print("Readying Up")
        from Backend.gameboardGroupings.game_processor import GameProcessor

        self.game_processor = GameProcessor("1234")
 
    def get_game_processor(self):
        print("Got Game Processor")
        return self.game_processor