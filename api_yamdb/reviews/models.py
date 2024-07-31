from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import NAME_LENGTH, SLUG_LENGTH, TEXT_LIMIT
from .validators import year_validator

User = get_user_model()


class CategoryGenreAbstract(models.Model):
    slug = models.SlugField('Слаг', unique=True, max_length=SLUG_LENGTH)
    name = models.CharField('Название', max_length=NAME_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name', )

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
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
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


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres',
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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(PubDateMixin, models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзывы'
    )
    text = models.TextField(verbose_name='Техт отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
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
        return self.text[:TEXT_LIMIT]


class Comment(PubDateMixin, models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:TEXT_LIMIT]

    class Meta(PubDateMixin.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
