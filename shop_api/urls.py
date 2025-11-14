"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Добавляем include для подключения приложений
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Маршруты для пользователей (регистрация, подтверждение, авторизация)
    path('api/v1/users/', include('users.urls')),
    
    # Старые маршруты (для совместимости)
    path('api/v1/product/', views.product_create_list, name='product-list-old'),
    path('api/v1/product/<int:id>/', views.product_detail, name='product-detail-old'),
    path('api/v1/category/', views.category_create_list, name='category-list-old'),
    path('api/v1/category/<int:id>/', views.category_detail, name='category-detail-old'),
    path('api/v1/review/', views.review_create_list, name='review-list-old'),
    path('api/v1/review/<int:id>/', views.review_detail, name='review-detail-old'),
    
    # Новые маршруты согласно домашнему заданию 3
    path('api/v1/categories/', views.category_create_list, name='categories-list'),
    path('api/v1/categories/<int:id>/', views.category_detail, name='categories-detail'),
    path('api/v1/products/', views.product_create_list, name='products-list'),
    path('api/v1/products/<int:id>/', views.product_detail, name='products-detail'),
    path('api/v1/reviews/', views.review_create_list, name='reviews-list'),
    path('api/v1/reviews/<int:id>/', views.review_detail, name='reviews-detail'),
    
    # Специальные эндпоинты
    path('api/v1/products/reviews/', views.products_with_reviews, name='products-with-reviews'),
]
