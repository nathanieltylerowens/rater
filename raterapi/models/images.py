from django.db import models
from django.db.models import CASCADE, DO_NOTHING

class GameImage(models.Model):
    action_pic = models.ImageField(upload_to='actionimages', height_field=None, width_field=None, max_length=None, null=True)
    game = models.ForeignKey("Game", on_delete=DO_NOTHING, related_name='pictures')