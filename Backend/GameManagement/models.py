import string
from typing import List
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import string

PASSCODE_LEN = 6
GAME_ID_LEN = 8
MAX_ATTEMPTS = 5

class GameRoom(models.Model):
    name = models.CharField(max_length=100)
    game_id = models
    address = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_rooms")
    status = models.PositiveIntegerField()
    players = models.ManyToManyField(User, related_name="game_rooms", blank=True, max_length=4)
    player_count = models.IntegerField(default=0, max_length=4)
    is_discoverable = models.BooleanField(default=False)
    passcode = models.CharField(max_length=100)
    is_password = models.BooleanField(default=False)
    max_players = models.IntegerField(default=4)

    def set_game_id(self, game_id) -> bool:
        is_success = False
        if len(game_id) == GAME_ID_LEN:
            if not self.is_id_used(game_id):
                self.game_id = game_id
                self.save()

        return is_success
    
    def is_id_used(self, game_id: str) -> bool:
        return GameRoom.objects.select_for_update(skip_locked=True).filter(game_id=game_id).exists()

# may be better to use uuid and make it smaller
    def generate_game_id(self, id_len: int = GAME_ID_LEN, max_attempts: int = MAX_ATTEMPTS) -> str:
        characters = string.ascii_uppercase + string.digits
        attempts = 0
        is_success = False
        game_id = ""
        # this could cause an error
        while not is_success and attempts < max_attempts:
            with transaction.atomic():
                game_id = ''.join(random.choice(characters, k=id_len))
                if self.is_id_used(game_id):
                    attempts += 1
                else:
                    #raising an exception may be safe handling of this function.
                    game_id = ""
                    is_success = True
        return game_id
                    
    def generate_passcode(self, max_len: int = PASSCODE_LEN) -> str:
        characters = string.digits
        passcode = "".join(random.choice(characters, k=max_len))
        return passcode

    def set_game_status(status_id) -> bool:
        pass
        
    def set_game_status(status_name) -> bool:
        pass
    def get_game_statues(self) -> List[str]:
        pass

    def get_game_status(self, status_id: int) -> str:
        pass

    def set_max_players(self, max_players: int):
        self.max_players = max_players
        self.save()
        

    def add_to_player_count(self):
        pass

    def remove_from_player_count(self):
        pass

    def is_discoverable(self):
        pass

    def is_password(self):
        pass

    def set_passcode(self, passcode: str) -> str:
        return len(passcode) <= PASSCODE_LEN and passcode.isdigit()

    def is_valid_passcode(self):
        pass

    def is_passcode_correct(self, passcode: str) -> bool:
        pass

    def __str__(self):
        return self.name



class GameStatus(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_stats", unique=True, primary_key=True)
    total_games = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    play_time = models.DurationField(default=timedelta(seconds=0))

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()
    
    def calculate_session_time(self):
        current_time = timezone.now()
        session_duration = current_time - self.last_login
        self.play_time += session_duration
        self.save()
    
    def get_formatted_playtime(self):
        total_seconds = int(self.play_time.total_seconds())
        # performs integer division to remove
        # remainder from division operation.
        days = total_seconds // 86400
        remaining = total_seconds % 86400
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60
        return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def add_win(self):
        self.wins += 1
        self.total_games += 1
        self.save()
    
    def add_loss(self):
        self.losses += 1
        self.total_games += 1
        self.save()
    
    def add_draw(self):
        self.draw += 1
        self.total_games += 1
        self.save()
    
    def __str__(self):
        return f"Statistics for {self.user.username}"