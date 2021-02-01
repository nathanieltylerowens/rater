from django.db import models
from raterapi.models.ratings import Ratings
class Game(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.DateField()
    number_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age = models.IntegerField()
    categories = models.ManyToManyField("Categories", related_name="game_categories", related_query_name="game_category")

    @property
    def avg_rating(self):
        ratings = Ratings.objects.filter(game_id=self.id)

        if len(ratings):
            sum_of_ratings = 0
            for rating in ratings:
                sum_of_ratings += rating.rating
            avg = sum_of_ratings / len(ratings)
            return round(float(avg), 1)
        return 30