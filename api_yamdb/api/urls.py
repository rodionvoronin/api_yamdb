from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet


app_name = 'api'

router = DefaultRouter()
router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/auth/token/', <Написать из views>.as_view(), name='get_token'),
    # path('v1/auth/signup/', <Написать из views>.as_view(), name='signup'),
]
