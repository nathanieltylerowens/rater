import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapi.models import Categories, Ratings, Game, Player
from django.contrib.auth.models import User


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types

        user = User()
        user.save()

        player = Player()
        player.user = user
        player.save()

        game_category = Categories()
        game_category.category = "Board game"
        game_category.save()

        game = Game()
        game.title = "Jimmy Dean of Students"
        game.number_of_players = 4
        game.time_to_play = 4
        game.age = 13
        game.designer = "Milton's Red Stapler"
        game.year_released = "1999-12-29"
        game.description = "PC Load letter? What does that even mean?"
        game.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "category_id": 1,
            "title": "ClueLess",
            "description": "as if",
            "designer": "Bradley Cooper",
            "year_released": "1999-12-29",
            "time_to_play": 6,
            "number_of_players": 4,
            "age": 9,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "ClueLess")
        self.assertEqual(json_response["description"], "as if")
        self.assertEqual(json_response["designer"], "Bradley Cooper")
        self.assertEqual(json_response["year_released"], "1999-12-29")
        self.assertEqual(json_response["time_to_play"], 6)
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["age"], 9)

    def test_delete_game(self):
        game = Game()
        game.title = "Jimmy Dean of Students"
        game.number_of_players = 4
        game.time_to_play = 4
        game.age = 13
        game.designer = "Milton's Red Stapler"
        game.year_released = "1999-12-29"
        game.description = "PC Load letter? What does that even mean?"
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_add_game_rating(self):
        url = "/rating"
        data = {
          "rating": 2,
          "player": 1,
          "game": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["rating"], 2)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["game"], 1)

    def test_get_single_game(self):
        game = Game()
        game.title = "Jimmy Dean of Students"
        game.number_of_players = 4
        game.time_to_play = 4
        game.age = 13
        game.designer = "Milton's Red Stapler"
        game.year_released = "1999-12-29"
        game.description = "PC Load letter? What does that even mean?"
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "Jimmy Dean of Students")
        self.assertEqual(json_response["description"], "PC Load letter? What does that even mean?")
        self.assertEqual(json_response["designer"], "Milton's Red Stapler")
        self.assertEqual(json_response["year_released"], "1999-12-29")
        self.assertEqual(json_response["time_to_play"], 4)
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["age"], 13)

    def test_add_game_review(self):
        url = "/reviews"
        data = {
          "review": "I really enjoyed this game",
          "player": 1,
          "gameId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["review"], "I really enjoyed this game")
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["game"], 1)

    def test_change_rating(self):
        rating = Ratings()
        rating.rating = 8
        rating.player = Player.objects.get(pk=1)
        rating.game = Game.objects.get(pk=1)
        rating.save()

        data = {
          "rating": 2,
          "player": 1,
          "game": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)
        response = self.client.put(f"/rating/{rating.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/rating/{rating.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["rating"], 2)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["game"], 1)

    def test_get_all_games(self):
        for i in range(1):
            game = Game()
            game.title = "Jimmy Dean of Students"
            game.number_of_players = 4
            game.time_to_play = 4
            game.age = 13
            game.designer = "Milton's Red Stapler"
            game.year_released = "1999-12-29"
            game.description = "PC Load letter? What does that even mean?"
            game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(1):
            self.assertEqual(json_response["results"][i]["title"], "Jimmy Dean of Students")
            self.assertEqual(json_response["results"][i]["description"], "PC Load letter? What does that even mean?")
            self.assertEqual(json_response["results"][i]["designer"], "Milton's Red Stapler")
            self.assertEqual(json_response["results"][i]["year_released"], "1999-12-29")
            self.assertEqual(json_response["results"][i]["time_to_play"], 4)
            self.assertEqual(json_response["results"][i]["number_of_players"], 4)
            self.assertEqual(json_response["results"][i]["age"], 13)
