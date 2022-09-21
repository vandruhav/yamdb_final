"""Модели приложения 'reviews'."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import CustomUser as User


class Categories(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес категории'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genres(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(fields=['name', 'year', 'category'],
                                    name='unique_title')
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связей произведений с жанрами."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre_id = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Произведение-жанр'
        verbose_name_plural = 'Произведения-жанры'


class Review(models.Model):
    title = models.ForeignKey(Title, models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации, отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')


class Comments(models.Model):
    """Модель комментариев."""
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации, комента',
        auto_now_add=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Комент'
        verbose_name_plural = 'Коменты'
