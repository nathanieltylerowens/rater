from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, GameImage
import uuid
import base64
from django.core.files.base import ContentFile

class ImageViewSet(ViewSet):

    def create(self, request):
        image = GameImage()
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')
        image.action_pic = data
        game = Game.objects.get(pk=request.data["gameId"])
        image.game = game

        try:
            image.save()
            serializer = ImageSerializer(image, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = ('id', 'game', 'action_pic')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
        depth = 1