from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Player
from raterapi.models.reviews import Reviews
from raterapi.views.game import GameSerializer


class ReviewsViewSet(ViewSet):

    def create(self, request):
        player = Player.objects.get(user=request.auth.user)
        reviews = Reviews()
        reviews.review = request.data["review"]
        game = Game.objects.get(pk=request.data["gameId"])
        reviews.game = game
        reviews.player = player

        try:
            reviews.save()
            serializer = ReviewSerializer(reviews, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            review = Reviews.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        reviews = Reviews.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            reviews = reviews.filter(gameId=game)

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('id', 'review', 'player', 'game')

class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ReviewPlayerSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user', 'game_id', 'player_id']
        depth = 2

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
        depth = 1