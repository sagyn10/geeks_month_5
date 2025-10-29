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
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('api/v1/product/', views.product_list, name='product-list'),
    path('api/v1/product/<int:id>/', views.product_detail, name='product-detail'),
    
 
    path('api/v1/category/', views.category_list, name='category-list'),
    path('api/v1/category/<int:id>/', views.catgory_detail, name='category-detail'),
    
  
    path('api/v1/review/', views.review_list, name='review-list'),
    path('api/v1/review/<int:id>/', views.review_detail, name='review-detail'),
    
    
    path('api/v1/products/reviews/', views.products_with_reviews, name='products-with-reviews'),
    path('api/v1/categories/', views.categories_with_count, name='categories-with-count'),
]
