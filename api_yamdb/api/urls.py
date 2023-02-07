from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet,
)

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
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    ReviewViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/auth/token/', <Написать из views>.as_view(), name='get_token'),
    # path('v1/auth/signup/', <Написать из views>.as_view(), name='signup'),
]
