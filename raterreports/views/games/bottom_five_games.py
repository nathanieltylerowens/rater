import sqlite3
from django.shortcuts import render
from raterapi.models import Game, Ratings
from raterreports.views import Connection

def bottom_five_games(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    g.title Title,
                    ROUND(AVG(r.rating),2) AverageRating,
                    g.id game_id
                FROM
                    raterapi_game g
                JOIN
                    raterapi_ratings r ON r.game_id = g.id
                GROUP BY g.id
                ORDER BY AverageRating ASC
                LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            bottom_five_list = {}

            for row in dataset:
                game_id = row["game_id"]
                average_rating = row["AverageRating"]
                title = row["Title"]

                bottom_five_list[game_id] = {}
                bottom_five_list[game_id]["id"] = game_id
                bottom_five_list[game_id]["rating"] = average_rating
                bottom_five_list[game_id]["title"] = title

        list_of_bottom_five_games = bottom_five_list.values()
        template = 'games/bottom_five_list.html'
        context = {
            'bottom_five_games': list_of_bottom_five_games
        }

        return render(request, template, context)