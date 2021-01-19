from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DISTRICTS = [
    ('Алтыарыкский район', 'Алтыарыкский район'),
    ('Багдадский район', 'Багдадский район'),
    ('Бешарыкский район', 'Бешарыкский район'),
    ('Бувайдинский район', 'Бувайдинский район'),
    ('Язъяванский район', 'Язъяванский район'),
    ('Ферганский район', 'Ферганский район'),
    ('Дангаринский район', 'Дангаринский район'),
    ('Фуркатский район', 'Фуркатский район'),
    ('Куштепинский район', 'Куштепинский район'),
    ('Кувинский район', 'Кувинский район'),
    ('Риштанский район', 'Риштанский район'),
    ('Сохский район', 'Сохский район'),
    ('Ташлакский район', 'Ташлакский район'),
    ('Учкуприкский район', 'Учкуприкский район'),
    ('Узбекистанский район', 'Узбекистанский район'),
]

DEFAULT_TYPES_OF_SHOPS = [
    ('Cупермаркет', 'Супермаркет'),
    ('Гипермаркет', 'Гипермаркет'),
    ('Хозяйственный магазин', 'Хозяйственный магазин'),
    ('Универсальный магазин', 'Универсальный магазин'),
    ('Бутик', 'Бутик'),
    ('Бакалея', 'Бакалея'),
    ('Зоомагазин', 'Зоомагазин'),
]

DEFAULT_TYPES_OF_GOODS = [
    ('', ''),
    ('Напитки', 'Напитки'),
    ('Еда', 'Еда'),
    ('Овощи', 'Овощи')
]

class District(models.Model):
    name = models.CharField(max_length=255, verbose_name="Район", unique=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    patronymic = models.CharField(max_length=255, blank=False, verbose_name="Отчество")
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True, verbose_name='Номер телефона')
    districts = models.JSONField(verbose_name="Районы")
    password = models.CharField(max_length=50, verbose_name="Пароль", blank=False)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.patronymic}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'


class Good(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    price_for_one = models.FloatField(max_length=10, blank=False, verbose_name='Цена за штуку')
    price_for_wholesaler = models.FloatField(max_length=10, blank=False, verbose_name='Цена для оптовика')
    description = models.TextField(null=True, verbose_name='Описание')
    min_quantity_to_buy = models.IntegerField(verbose_name='Минимальное количество для покупки')
    quantity = models.IntegerField(verbose_name='Количество')
    photo = models.ImageField(upload_to='goods/', blank=True, verbose_name='Фотография')

    def __str__(self):
        return f"{self.category} - {self.category}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Shop(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name='Название', null=False)
    inn = models.CharField(max_length=20, verbose_name="ИНН", null=False, unique=True)
    phone_number = models.CharField(max_length=15, null=False, unique=True, verbose_name='Номер телефона')
    district = models.CharField(max_length=6, verbose_name="Район")
    address = models.CharField(max_length=255, verbose_name="Адресс", null=False)
    landmark = models.CharField(max_length=255, verbose_name='Ориентир', null=False)
    category = models.CharField(max_length=6, verbose_name="Категория", null=False)
    token = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'