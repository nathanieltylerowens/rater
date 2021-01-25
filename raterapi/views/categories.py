from django.http import HttpResponse
from rest_framework.viewsets import ViewSet 
from rest_framework.response import Response 
from rest_framework import serializers
from raterapi.models import Categories as CategoriesModel

class Categories(ViewSet):
    def retrive(self, request, pk=None):
        try:
            category = CategoriesModel.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex) 


    def list(self, request):
        categories = CategoriesModel.objects.all()

        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesModel
        fields = ('id', 'name')