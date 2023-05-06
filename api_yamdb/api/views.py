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

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view
from django.db import IntegrityError
from api.permissions import IsAdminOrSuperUser
from api.serializers import RegistrationSerializer
from api.serializers import TokenSerializer, UserSerializer
from api.serializers import UserEditSerializer
from reviews.models import User
from rest_framework.pagination import PageNumberPagination


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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Регистрация пользователя"""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, _ = User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        return Response('Это имя или email уже занято',
                        status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на сайте YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Получение jwt токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Администратор получает список пользователей или создает нового"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperUser,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch', ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],)
    def me_info(self, request):
        user = request.user
        if user.is_authenticated:
            if request.method == "GET":
                serializer = UserSerializer(
                    user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if request.method == "PATCH":
                serializer = UserEditSerializer(
                    user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)
