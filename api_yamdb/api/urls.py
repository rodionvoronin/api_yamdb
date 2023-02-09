from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('v1/titles', TitleViewSet)
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    'v1/users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
