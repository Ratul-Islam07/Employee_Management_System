from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:pk>/', views.profile, name='profile_page'),
    path('add/', views.add_employee, name='add_employee'),
    path('update/', views.update, name='update_page'),
    path('update/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete/', views.delete, name='delete_page'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
]
