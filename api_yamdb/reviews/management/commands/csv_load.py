import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


User = get_user_model()


def category_create(row):
    """Функция для создания категории"""
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_create(row):
    """Функция для создания жанра"""
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def titles_create(row):
    """Функция для создания произведения"""
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def users_create(row):
    """Функция для создания пользователя"""
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def review_create(row):
    """Функция для создания отзыва"""
    title, _ = Title.objects.get_or_create(id=row[1])
    Review.objects.get_or_create(
        id=row[0],
        title=title,
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comment_create(row):
    """Функция для создания комментария"""
    review, _ = Review.objects.get_or_create(id=row[1])
    Comment.objects.get_or_create(
        id=row[0],
        review=review,
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


def genre_title_create(row):
    """Функция для создания связи между жанром и произведением"""
    title, _ = Title.objects.get_or_create(id=row[1])
    genre, _ = Genre.objects.get_or_create(id=row[2])
    GenreTitle.objects.get_or_create(
        id=row[0],
        title=title,
        genre=genre,
    )


action = {
    """Словарь, где ключ - имя файла,
    а значение - функция для создания объектов"""

    'category.csv': category_create,
    'genre.csv': genre_create,
    'titles.csv': titles_create,
    'users.csv': users_create,
    'review.csv': review_create,
    'comments.csv': comment_create,
    'genre_title.csv': genre_title_create
}


class Command(BaseCommand):
    """Класс команды для загрузки данных в базу данных"""
    help = "Load test DB from dir (../static/data/)"

    def handle(self, *args, **options):
        for filename, row in action.items():
            path = os.path.join(settings.BASE_DIR, "static/data/") + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    action[filename](row)
        self.stdout.write("!!!The database has been loaded successfully!!!")
