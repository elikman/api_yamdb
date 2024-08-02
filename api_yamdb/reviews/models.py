from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse

from .constants import NAME_LENGTH, SLUG_LENGTH, TEXT_LENGTH
from .validators import year_validator

User = get_user_model()


class CategoryGenreAbstract(models.Model):
    """Абстрактная модель для категорий и жанров"""
    slug = models.SlugField('Слаг', unique=True, max_length=SLUG_LENGTH)
    name = models.CharField('Название', max_length=NAME_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenreAbstract):
    "Категории произведений"

    class Meta(CategoryGenreAbstract.Meta):
        verbose_name = 'Название'
        verbose_name_plural = 'Названия категорий'


class Genre(CategoryGenreAbstract):
    "Жанры произведений"

    class Meta(CategoryGenreAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    "Произведения"
    name = models.CharField('Произведение', max_length=NAME_LENGTH)
    year = models.SmallIntegerField('Год выпуска', db_index=True,
                                    validators=[year_validator])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres_titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='category_titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('title_detail', args=[str(self.id)])

    def get_average_score(self):
        return self.reviews.aggregate(Avg('score'))['score__avg']


class GenreTitle(models.Model):
    """Модель жанра произведения"""
    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genre_titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_combination_gt'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'


class PubDateMixin(models.Model):
    """Абстрактная модель для дат публикации"""
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(PubDateMixin, models.Model):
    """Модель отзыва"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзывы'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta(PubDateMixin.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Comment(PubDateMixin, models.Model):
    """Модель комментария"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )

    def __str__(self):
        return self.text[:TEXT_LENGTH]

    class Meta(PubDateMixin.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
