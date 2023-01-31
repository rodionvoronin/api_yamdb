from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet


app_name = 'api'

router = DefaultRouter()
router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
