from django.urls import include, path
from rest_framework import routers
from api.views import registration, get_jwt_token
from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'user')
router.register('categories', CategoriesViewSet, 'categories')
router.register('genres', GenresViewSet, 'genres')
router.register('titles', TitleViewSet, 'titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
