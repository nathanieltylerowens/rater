import sqlite3
from django.shortcuts import render
from raterapi.models import Game, Ratings
from raterreports.views import Connection

def top_three_reviewers(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
              SELECT 
                  COUNT(r.player_id) review_count, u.id user, u.first_name || ' ' || u.last_name AS full_name
              FROM raterapi_reviews r 
              JOIN auth_user u ON u.id = r.player_id
              GROUP BY r.player_id
              ORDER BY review_count DESC
              LIMIT 3
            """)

            dataset = db_cursor.fetchall()

            most_reviews = {}

            for row in dataset:
                user = row["user"]
                review_count = row["review_count"]
                name = row["full_name"]

                most_reviews[user] = {}
                most_reviews[user]["id"] = user
                most_reviews[user]["review_count"] = review_count
                most_reviews[user]["full_name"] = name

        list_of_top_three_reviewers = most_reviews.values()
        template = 'games/most_reviews.html'
        context = {
            'top_three_reviewers': list_of_top_three_reviewers
        }

        return render(request, template, context)