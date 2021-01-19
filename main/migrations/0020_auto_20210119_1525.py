# Generated by Django 3.1.5 on 2021-01-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210119_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='inn',
            field=models.CharField(max_length=20, unique=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='token',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]