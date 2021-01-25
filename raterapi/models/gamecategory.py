from django.db import models
from django.db.models import CASCADE

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    category = models.ForeignKey("Categories", on_delete=CASCADE)