from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Goods, Shops, UserProfile
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import forms
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
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
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    form = UserProfileForm
    verbose_name_plural = 'Необходимые данные'
    

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'groups'),
        }),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    inlines = (UserProfileInline,)
    ordering = ['id']

    def get_full_name(self, obj):
        user = UserProfile.objects.get(user=obj)
        patronymic = user.patronymic
        return "%s %s %s" % (obj.last_name, obj.first_name, patronymic)

    get_full_name.short_description = "Полное имя"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inn', 'phone_number', 'district', 'address', 'landmark', 'get_type')
    search_fields = ['id', 'name', 'inn', 'phone_number', 'district', 'address', 'landmark']
    fieldsets = (
        ("Важная информация", {
            "fields": ("name", "inn", "phone_number")
        }),
        ("Локация", {
            "fields": ("address", "geolocation", "landmark")
        }), 
        ("Вид", {
            "fields": ("type_of", "additional_type")
        })
    )
    
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

    def get_type(self, obj):
        if obj.type_of == '' and obj.additional_type != '':
            return obj.additional_type
        elif obj.type_of != '':
            return obj.type_of
    get_type.short_description = "Тип"

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price_for_one', 'description', 'quantity')


# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)


# Register your models here.
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(User, UserAdmin)