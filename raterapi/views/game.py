from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet 
from rest_framework.response import Response 
from rest_framework import serializers 
from raterapi.models import Game, Categories


class Games(ViewSet):

    def create(self, request):
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.time_to_play = request.data["timeToPlay"]
        game.age = request.data["age"]
        categories = Categories.objects.get(pk=request.data["categoryId"])

        try: 
            game.save()
            game.categories.add(categories)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        games = Game.objects.all()

        serializer = GameSerializer(
          games, many=True, context={'request': request})
        return Response(serializer.data)

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categories
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True)

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'designer', 'year_released', 'number_of_players', 'time_to_play', 'age', 'categories', 'reviews')
        depth = 1