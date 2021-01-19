from django.urls import path
from . import views

urlpatterns = [
    path('get_districts/', views.get_districts),
    path('<int:user_id>/get_all_data/', views.get_all_data),
    path('submit_user/', views.submit_user),
    path("<int:user_id>/change_user/", views.change_user)
]