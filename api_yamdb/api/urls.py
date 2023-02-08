from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    APIGetToken, APISignup, CategoryViewSet,
    CommentViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UsersViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('v1/titles', TitleViewSet, basename='titles')
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('v1/users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
