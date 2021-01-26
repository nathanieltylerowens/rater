from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from raterapi.views import register_user, login_user, Games, Categories, ReviewsViewSet, ImageViewSet, RatingViewSet
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'categories', Categories, 'category')
router.register(r'reviews', ReviewsViewSet, 'review')
router.register(r'image', ImageViewSet, 'image')
router.register(r'rating', RatingViewSet, 'rating')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)