import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

DATA_DIR = os.path.join(settings.BASE_DIR, "static/data/")

User = get_user_model()


def create_object(filename, func):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            func(row)


def category_create(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_create(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def titles_create(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def users_create(row):
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
    review, _ = Review.objects.get_or_create(id=row[1])
    Comment.objects.get_or_create(
        id=row[0],
        review=review,
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


def genre_title_create(row):
    title, _ = Title.objects.get_or_create(id=row[1])
    genre, _ = Genre.objects.get_or_create(id=row[2])
    GenreTitle.objects.get_or_create(
        id=row[0],
        title=title,
        genre=genre,
    )


action = {
    'category.csv': category_create,
    'genre.csv': genre_create,
    'titles.csv': titles_create,
    'users.csv': users_create,
    'review.csv': review_create,
    'comments.csv': comment_create,
    'genre_title.csv': genre_title_create
}


class Command(BaseCommand):
    help = "Load test DB from dir ({})".format(DATA_DIR)

    def handle(self, *args, **options):
        for filename, func in action.items():
            create_object(filename, func)
        self.stdout.write("!!!База данных загружена успешно!!!")
