from django.db import models
from django.db.models import CASCADE

class Images(models.Model):
    image_url = models.CharField(max_length=100)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)