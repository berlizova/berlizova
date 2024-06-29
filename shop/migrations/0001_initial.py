# Generated by Django 5.0.6 on 2024-06-22 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('opening_days', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='news_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProdCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('sort', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField(blank=True, default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='staff_photo/')),
                ('bio', models.TextField()),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Персонал магазина',
                'verbose_name_plural': 'Персонал магазина',
            },
        ),
        migrations.CreateModel(
            name='Prod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_visible', models.BooleanField(default=True)),
                ('sort', models.PositiveSmallIntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='prods/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prods', to='shop.prodcategory')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['sort'],
            },
        ),
    ]
