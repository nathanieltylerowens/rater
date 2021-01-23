from django.db import models
from django.db.models import CASCADE

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    player = models.ForeignKey("Player", on_delete=CASCADE)