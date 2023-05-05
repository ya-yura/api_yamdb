from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from reviews.models import Category, Genre, Review, Title
from .serializers import CategorySerializer, GenreSerializer, TitleCreateSerializer, TitleDisplaySerializer


class CategoriesViewSet():
    """Вьюсет категорий произведений."""
    permission_classes = [
        IsAdminOrReadOnly
    ]
    filter_backends = (
        filters.SearchFilter,
    )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = (
        'name', '=slug'
    )
    lookup_field = 'slug'


class GenresViewSet():
    """Вьюсет жанра произведений."""
    permission_classes = [
        IsAdminOrReadOnly
    ]
    filter_backends = (
        filters.SearchFilter,
    )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        '=name',
    )


class TitleViewSet():
    """Вьюсет произведений."""
    permission_classes = [
        IsAdminOrReadOnly
    ]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    pagination_class = LimitOffsetPagination


    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleDisplaySerializer
        else:
            self.action in ['create', 'update', 'partial_update']
            return TitleCreateSerializer


class CommentViewSet():
    pass


class ReviewViewSet():
    pass


class UserViewSet():
    pass


class signup():
    pass


class token():
    pass