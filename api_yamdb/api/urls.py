from django.urls import include, path
from rest_framework import routers
from api.views import registration, UserViewSet, get_jwt_token

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
