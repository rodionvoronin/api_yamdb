from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, CategoryViewSet,
                    CommentViewSet, GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet, signup)

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
router.register(
    'v1/users',
    UserViewSet,
    basename='users'
)

auth_urlpatterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', signup, name='signup'),
]


urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]
