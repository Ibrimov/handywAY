# Generated by Django 3.1.5 on 2021-01-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210119_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='district',
            field=models.CharField(default='', max_length=100, verbose_name='Район'),
        ),
    ]
