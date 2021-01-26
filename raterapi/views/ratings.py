from rest_framework import viewsets
from raterapi.models import Ratings
from rest_framework import serializers

class RatingsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Ratings
        fields = ('id', 'rating', 'player', 'game')

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer