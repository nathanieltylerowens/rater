import sqlite3
from django.shortcuts import render
from raterreports.views import Connection

def most_reviewed_game(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT MAX(number_of_reviews) review_count, title, game_id
                FROM
                (SELECT g.title title, COUNT(r.id) number_of_reviews, g.id game_id
                FROM raterapi_reviews r 
                JOIN raterapi_game g on g.id = r.game_id
                GROUP BY g.id )
            """)

            dataset = db_cursor.fetchall()

            reviewed_game = {}

            for row in dataset:
                game_id = row["game_id"]
                game_title = row["title"]
                number_of_reviews = row["review_count"]

                reviewed_game[game_id] = {}
                reviewed_game[game_id]["game_title"] = game_title
                reviewed_game[game_id]["review_count"] = number_of_reviews

        top_game = reviewed_game.values()
        template = 'games/most_reviewed_game.html'
        context = {
            'most_reviewed_game': top_game
        }

        return render(request, template, context)