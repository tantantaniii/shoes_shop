# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.shoe_list, name='shoe_list'),
    path('shoe/<int:pk>/', views.shoe_detail, name='shoe_detail'),

    # Корзина
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:shoe_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:shoe_id>/<str:size>/', views.cart_remove, name='cart_remove'),

    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]