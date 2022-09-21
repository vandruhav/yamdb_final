import csv

from django.core.management.base import BaseCommand
from reviews.models import (Categories, Comments, Genres, GenreTitle, Review,
                            Title)
from users.models import CustomUser as User

file_table = {
    'category.csv': Categories,
    'genre.csv': Genres,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comments
}


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        for file, table in file_table.items():
            with open(f'static/data/{file}', 'r', encoding='utf8') as f:
                dr = csv.DictReader(f, delimiter=',')
                for row in dr:
                    if file == 'titles.csv':
                        category = Categories.objects.get(
                            id=row.pop('category'))
                        table.objects.get_or_create(category=category, **row)
                    elif file == 'genre_title.csv':
                        title = Title.objects.get(id=row.pop('title_id'))
                        genre = Genres.objects.get(id=row.pop('genre_id'))
                        table.objects.get_or_create(title_id=title,
                                                    genre_id=genre, **row)
                    elif file == 'review.csv':
                        title = Title.objects.get(id=row.pop('title_id'))
                        author = User.objects.get(id=row.pop('author'))
                        table.objects.get_or_create(title=title, author=author,
                                                    **row)
                    elif file == 'comments.csv':
                        review = Review.objects.get(id=row.pop('review_id'))
                        author = User.objects.get(id=row.pop('author'))
                        table.objects.get_or_create(review_id=review,
                                                    author=author, **row)
                    else:
                        table.objects.get_or_create(**row)
                self.stdout.write(f'Таблица {table.__name__} заполнена!')
