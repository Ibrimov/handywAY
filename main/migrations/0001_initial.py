# Generated by Django 3.1.5 on 2021-01-18 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Район')),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('category', models.CharField(choices=[('', ''), ('Напитки', 'Напитки'), ('Еда', 'Еда'), ('Овощи', 'Овощи')], default='', max_length=50, verbose_name='Категория')),
                ('price_for_one', models.FloatField(max_length=10, verbose_name='Цена за штуку')),
                ('price_for_wholesaler', models.FloatField(max_length=10, verbose_name='Цена для оптовика')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('min_quantity_to_buy', models.IntegerField(verbose_name='Минимальное количество для покупки')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('photo', models.ImageField(blank=True, upload_to='goods/', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('inn', models.IntegerField(verbose_name='ИНН')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')),
                ('district', models.CharField(choices=[('Алтыарыкский район', 'Алтыарыкский район'), ('Багдадский район', 'Багдадский район'), ('Бешарыкский район', 'Бешарыкский район'), ('Бувайдинский район', 'Бувайдинский район'), ('Язъяванский район', 'Язъяванский район'), ('Ферганский район', 'Ферганский район'), ('Дангаринский район', 'Дангаринский район'), ('Фуркатский район', 'Фуркатский район'), ('Куштепинский район', 'Куштепинский район'), ('Кувинский район', 'Кувинский район'), ('Риштанский район', 'Риштанский район'), ('Сохский район', 'Сохский район'), ('Ташлакский район', 'Ташлакский район'), ('Учкуприкский район', 'Учкуприкский район'), ('Узбекистанский район', 'Узбекистанский район')], default='', max_length=100, verbose_name='Район')),
                ('address', models.CharField(max_length=255, verbose_name='Адресс')),
                ('landmark', models.CharField(max_length=255, verbose_name='Ориентир')),
                ('type_of', models.CharField(choices=[('Cупермаркет', 'Супермаркет'), ('Гипермаркет', 'Гипермаркет'), ('Хозяйственный магазин', 'Хозяйственный магазин'), ('Универсальный магазин', 'Универсальный магазин'), ('Бутик', 'Бутик'), ('Бакалея', 'Бакалея'), ('Зоомагазин', 'Зоомагазин')], default='', max_length=100, verbose_name='Тип')),
                ('additional_type', models.CharField(blank=True, max_length=50, verbose_name='Другой тип (можете оставить пустым)')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patronymic', models.CharField(max_length=255, verbose_name='Отчество')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')),
                ('districts', models.JSONField(verbose_name='Районы')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
