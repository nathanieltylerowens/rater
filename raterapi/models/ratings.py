from django.db import models
from django.db.models import CASCADE

class Ratings(models.Model):
    rating = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)