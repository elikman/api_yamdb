# Generated by Django 3.2 on 2024-08-02 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20240710_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Название', 'verbose_name_plural': 'Названия категорий'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genretitle',
            options={'verbose_name': 'Жанр произведения', 'verbose_name_plural': 'Жанры произведения'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Слаг'),
        ),
    ]
