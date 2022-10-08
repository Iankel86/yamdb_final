# Generated by Django 2.2.16 on 2022-09-05 21:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import titles.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимый символ в slug категории.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('year', models.PositiveIntegerField(validators=[titles.validators.year_validator], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.Category', verbose_name='Категория произведения')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='titles.Genre', verbose_name='Жанр произведения')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('-id',),
            },
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='titles_genr_name_23d879_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='titles_cate_name_541465_idx'),
        ),
    ]