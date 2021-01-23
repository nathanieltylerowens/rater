from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.DateField()
    number_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age = models.IntegerField()