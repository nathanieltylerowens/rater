from django.urls import path
from .views import top_five_games, bottom_five_games,games_per_category, more_than_three, most_reviewed_game, under_eight_games, top_three_reviewers

urlpatterns = [
    path('reports/topfive', top_five_games),
    path('reports/bottomfive', bottom_five_games),
    path('reports/gamespercategory', games_per_category),
    path('reports/morethanthree', more_than_three),
    path('reports/mostreviewed', most_reviewed_game),
    path('reports/undereight', under_eight_games),
    path('reports/mostreviews', top_three_reviewers),
]