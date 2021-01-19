from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Good, Shop, UserProfile, Category, District
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import forms
from django.utils.translation import gettext, gettext_lazy as _

# Changing the frontend of admin panel
admin.site.site_header = "Панель Управления | HandyWay"
admin.site.site_title = "Панель Управления | HandyWay"
admin.site.index_title = "Панель Управления"
admin.site.site_url= None


# Configurations for Forms
class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.empty_permitted = False # Here

    class Meta:
        model = UserProfile
        fields = ('__all__')


# Configurations for frontend of models in admin panel
class UserAdmin(admin.ModelAdmin):
    change_form_template = "admin/userprofile_form.html"
    ordering = ['id']
    list_display = ["id", "get_full_name", "username", "get_password", "get_phone_number", "is_superuser"]
    list_display_links = ['id', 'get_full_name']

    def get_full_name(self, obj):
        user = UserProfile.objects.get(user=obj)
        patronymic = user.patronymic
        return "%s %s %s" % (obj.last_name, obj.first_name, patronymic)
    
    def get_password(self, obj):
        user = UserProfile.objects.get(user=obj)
        password = user.password
        return password
    get_password.short_description = "Пароль"
    
    def get_phone_number(self, obj):
        user = UserProfile.objects.get(user=obj)
        phone_number = user.phone_number
        return phone_number
    get_phone_number.short_description = "Номер"

    get_full_name.short_description = "Полное имя"

    def get_dynamic_info(self):
        # ...
        pass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_dynamic_info()

        return super(UserAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class ShopAdmin(admin.ModelAdmin):
    change_form_template = "admin/shop.html"
    list_display = ('id', 'name', 'inn', 'phone_number', 'get_district', 'address', 'landmark', 'get_category', 'added_by')
    ordering = ['id']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', 'inn', 'phone_number', 'get_district', 'address', 'landmark']

    def added_by(self, obj):
        shop = Shop.objects.get(id=obj.id)
        return shop.person.get_full_name()
    added_by.short_description = "Добавил"

    def get_category(self, obj):
        category = Category.objects.get(id=obj.category)
        return category
    get_category.short_description = "Тип"

    def get_district(self, obj):
        district = District.objects.get(id=obj.district)
        return district
    get_district.short_description = "Район"

    def get_dynamic_info(self):
        # ...
        pass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_dynamic_info()

        return super(ShopAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price_for_one', 'description', 'quantity')
    ordering = ['id']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', 'category']
    fieldsets = (
        ("Важные данные", {
            "fields": ("name", "category")
        }),
        ("Цена", {
            "fields": ("price_for_one", "price_for_wholesaler")
        }),
        ("Детали", {
            "fields": ("min_quantity_to_buy", "quantity")
        }), 
        ("Вид", {
            "fields": ("description", "photo")
        })
    )


# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Shop, ShopAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(District)
admin.site.register(Category)