from django.urls import include, path
from rest_framework.routers import SimpleRouter

# from .views import 

app_name = 'api'



urlpatterns = [
    # path('v1/auth/token/', <Написать из views>.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', <Написать из views>.as_view(), name='signup'),
]
