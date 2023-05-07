from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleDisplaySerializer,
                          CommentSerializer, ReviewSerializer)
from .permissions import (IsAdminOrReadOnly, IsStaffOrAuthorOrReadOnly)


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class UserViewSet():
    pass


class signup():
    pass


class token():
    pass
