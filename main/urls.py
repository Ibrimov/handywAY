from django.urls import path
from . import views

urlpatterns = [
    path('get_districts/', views.get_districts),
    path('get_categories/', views.get_categories),
    path('<int:user_id>/get_all_data_user/', views.get_all_data_user),
    path('submit_user/', views.submit_user),
    path('<int:user_id>/change_user/', views.change_user),
    path('<int:user_id>/delete_user/', views.delete_user),
    path('add_shop/', views.add_shop),
    path('<int:shop_id>/delete_shop/', views.delete_shop),
    path('<int:shop_id>/get_all_data_shop/', views.get_all_data_shop),
    path('<int:shop_id>/change_shop/', views.change_shop)
]