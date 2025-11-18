from django.urls import path, include
from product import views

urlpatterns = [
    # Основные CRUD операции для товаров
    path('', views.ProductListCreateView.as_view()),
    path('<int:id>/', views.ProductDetailView.as_view()),
    
    # Основные CRUD операции для категорий
    path('categories/', views.CategoryListCreateView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailView.as_view()),
    
    # Основные CRUD операции для отзывов
    path('reviews/', views.ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailView.as_view()),
    
    # Специальные endpoints
    path('with-reviews/', views.ProductsWithReviewsView.as_view()),
    path('categories/with-count/', views.CategoriesWithCountView.as_view()),
]