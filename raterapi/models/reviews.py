from django.db import models
from django.db.models import CASCADE

class Reviews(models.Model):
    review = models.TextField()
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)