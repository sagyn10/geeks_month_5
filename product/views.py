from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status               
from django.db.models import Avg, Count        
from .models import Product, Category, Review
from .serializers import (                     
    CategoryDetailSerializers, CategoryListSerializers,
    ProductDetailSerializers, ProductListSerializers,
    ReviewDetailSerializers, ReviewListSerializers,
    ProductWithReviewsSerializer, ProductSerializer,
    CategoryValidateSerializer, ProductValidateSerializer,
)
from django.db import transaction
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductListCreateView(ListCreateAPIView):
    """
    API для работы со списком товаров.
    GET - получить список всех товаров
    POST - создать новый товар
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers
    

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    API для работы с отдельным товаром.
    GET - получить товар по ID
    PUT - обновить товар
    DELETE - удалить товар
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers
    lookup_field = 'id'


class CategoryListCreateView(ListCreateAPIView):
    """
    API для работы со списком категорий.
    GET - получить список всех категорий с количеством товаров
    POST - создать новую категорию
    """
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategoryListSerializers


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    API для работы с отдельной категорией.
    GET - получить категорию по ID
    PUT - обновить категорию
    DELETE - удалить категорию
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializers
    lookup_field = 'id'


class ReviewListCreateView(ListCreateAPIView):
    """
    API для работы со списком отзывов.
    GET - получить список всех отзывов
    POST - создать новый отзыв
    """
    queryset = Review.objects.select_related('product')
    serializer_class = ReviewListSerializers


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    API для работы с отдельным отзывом.
    GET - получить отзыв по ID
    PUT - обновить отзыв
    DELETE - удалить отзыв
    """
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers 
    lookup_field = 'id'


class ProductsWithReviewsView(APIView):
    """
    Специальный эндпоинт для получения товаров с отзывами и рейтингом.
    GET - возвращает список всех товаров с их отзывами и средним рейтингом
    """
    def get(self, request):
        # prefetch_related оптимизирует загрузку связанных отзывов
        # annotate добавляет вычисляемое поле average_rating (средний рейтинг)
        products = Product.objects.prefetch_related('reviews').annotate(
            average_rating=Avg('reviews__stars')  # Avg вычисляет среднее значение звезд
        )
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class CategoriesWithCountView(APIView):
    """
    Альтернативный эндпоинт для категорий с подсчетом товаров.
    GET - возвращает список всех категорий с количеством товаров в каждой
    """
    def get(self, request):
        # annotate добавляет к каждой категории подсчет количества товаров
        categories = Category.objects.annotate(
            products_count=Count('products')  # Count считает связанные товары через ForeignKey
        )
        data = CategoryListSerializers(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)