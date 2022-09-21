"""Представления приложения 'api'."""
from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Comments, Genres, Review, Title

from api_yamdb import settings

from .custom_viewsets import ListCreateDeleteViewSet
from .filters import TitleFilter
from .permissions import (AdminOrReadOnly, AuthorOrReadOnly, OnlyAdmin,
                          OnlyAdminCanGiveRole)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleROSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)

User = get_user_model()


def get_usr(self):
    return get_object_or_404(
        User,
        username=self.request.user,
    )


class CategoriesViewSet(ListCreateDeleteViewSet):
    """Представление для работы с категориями."""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(ListCreateDeleteViewSet):
    """Представление для работы с жанрами."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с произведениями."""
    queryset = Title.objects.all().annotate(Avg("review__score")).order_by(
        "id")
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Функция выбора сериализатора."""
        if self.action in ('list', 'retrieve'):
            return TitleROSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для работы с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_title_id = self.kwargs.get("url_title_id")
        return Review.objects.filter(title_id=url_title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('url_title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=get_usr(self), title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление для работы с коментариями."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_review_id = self.kwargs.get("url_review_id")
        return Comments.objects.filter(review_id=url_review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("url_review_id")
        )
        serializer.save(author=get_usr(self), review_id=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Функция создает пользователя и
    отправляет ему на почту код подтверждения.
    """
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    body = {
        "username": username,
        "confirmation_code": confirmation_code
    }
    json_body = dumps(body)
    send_mail(
        subject="Подтверждение регистрации на сайте yamDB",
        message=(
            f"Добрый день, {username}!\n"
            f"Для подтверждения регистрации отправьте POST "
            f"запрос на http://{settings.DOMAIN}/api/v1/auth/token/ "
            f"в теле запроса передайте:\n"
            f"{json_body}"
        ),
        from_email=f"{settings.CONFIRM_EMAIL}",
        recipient_list=[request.data["email"]],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_view(request):
    """Получение токена при POST-запросе."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status.HTTP_200_OK)
    return Response("Неверный запрос", status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    permission_classes = (OnlyAdmin, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[
            IsAuthenticated,
            OnlyAdminCanGiveRole
        ]
    )
    def me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
