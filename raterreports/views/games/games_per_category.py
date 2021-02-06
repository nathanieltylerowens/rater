import sqlite3
from django.shortcuts import render
from raterreports.views import Connection

def games_per_category(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    gc.id,
                    c.id cat_id,
                    c.name CategoryName,
                    COUNT(g.id) NumberGames
                FROM raterapi_categories c 
                JOIN raterapi_game_categories gc ON gc.categories_id = c.id
                JOIN raterapi_game g ON g.id = gc.game_id
                GROUP BY c.id
            """)

            dataset = db_cursor.fetchall()

            category_list = {}

            for row in dataset:
                cat_id = row["cat_id"]
                games_in_cat = row["NumberGames"]
                cat_name = row["CategoryName"]

                category_list[cat_id] = {}
                category_list[cat_id]["games_in_cat"] = games_in_cat
                category_list[cat_id]["cat_name"] = cat_name

        list_of_games_per_category = category_list.values()
        template = 'games/games_per_category.html'
        context = {
            'games_per_category': list_of_games_per_category
        }

        return render(request, template, context)