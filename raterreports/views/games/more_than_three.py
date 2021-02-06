import sqlite3
from django.shortcuts import render
from raterreports.views import Connection

def more_than_three(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT g.title title, g.id game_id, g.number_of_players players
                FROM raterapi_game g
                WHERE g.number_of_players > 3
            """)

            dataset = db_cursor.fetchall()

            game_list = {}

            for row in dataset:
                game_id = row["game_id"]
                game_title = row["title"]
                player_count = row["players"]

                game_list[game_id] = {}
                game_list[game_id]["game_title"] = game_title
                game_list[game_id]["player_count"] = player_count

        more_than_three_players = game_list.values()
        template = 'games/more_than_three.html'
        context = {
            'more_than_three': more_than_three_players
        }

        return render(request, template, context)