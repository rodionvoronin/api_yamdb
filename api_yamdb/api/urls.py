from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'

router = DefaultRouter()
router.register('v1/titles', TitleViewSet)
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
