import sqlite3
from django.shortcuts import render
from raterreports.views import Connection

def under_eight_games(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT g.title title, g.id game_id, g.age age
                FROM raterapi_game g
                WHERE g.age < 8
            """)

            dataset = db_cursor.fetchall()

            under_eight_list = {}

            for row in dataset:
                game_id = row["game_id"]
                rec_age = row["age"]
                title = row["title"]

                under_eight_list[game_id] = {}
                under_eight_list[game_id]["id"] = game_id
                under_eight_list[game_id]["rec_age"] = rec_age
                under_eight_list[game_id]["title"] = title

        games_under_eight = under_eight_list.values()
        template = 'games/games_under_eight.html'
        context = {
            'under_eight_games': games_under_eight
        }

        return render(request, template, context)