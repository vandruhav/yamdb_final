"""Сериализаторы приложения 'api'."""
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comments, Genres, Review, Title

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, обновления и удаления произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Categories.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genres.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category'),
                message='Произведение уже существует!'
            )
        ]

    def validate_year(self, value):
        """Валидатор для поля года выпуска. Год выпуска - не больше текущего"""
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class TitleROSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(source='review__score__avg',
                                      read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)
        model = Review

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('url_title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Ревью уже существует!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для коментариев."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('review_id)',)
        model = Comments


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного польлзователя.
    Управление пользователем. Отправка эмэйла."
    """

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        """Проверка username !=me"""
        if not User.objects.filter(username=value).exists():
            if value.lower() == "me":
                raise serializers.ValidationError(
                    "Использовать имя 'me' в качестве username запрещено."
                )
            return value
        else:
            raise serializers.ValidationError('Пользователь уже существует.')

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            return value
        else:
            raise serializers.ValidationError(
                'Пользователь с таким емейл уже существует.'
            )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя."""
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор управления пользователем."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
