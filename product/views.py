from rest_framework.decorators import api_view  
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
from django.db import transaction  # Для атомарных операций с базой данных


@api_view(['GET', 'PUT', 'DELETE'])  # Декоратор указывает, какие HTTP методы поддерживает функция
def category_detail(request, id):
    """
    Обработка одной категории по ID.
    GET - получить категорию, PUT - обновить, DELETE - удалить
    """
    # Пытаемся найти категорию по ID
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        # Если категория не найдена, возвращаем 404
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Обработка GET запроса - возврат информации о категории
    if request.method == 'GET':
        data = CategoryDetailSerializers(category).data  # Преобразуем объект в JSON
        return Response(data=data, status=status.HTTP_200_OK)
    
    # Обработка PUT запроса - обновление категории
    elif request.method == 'PUT':
        name = request.data.get('name')  # Получаем новое имя из запроса
        category.name = name             # Обновляем имя
        category.save()                  # Сохраняем в базе данных
        data = CategoryDetailSerializers(category).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    # Обработка DELETE запроса - удаление категории
    elif request.method == 'DELETE':
        category.delete()  # Удаляем из базы данных
        return Response(status=status.HTTP_204_NO_CONTENT)  # 204 = успешное удаление

@api_view(['GET', 'POST'])  # Поддерживает GET (список) и POST (создание)
def category_create_list(request):
    """
    Работа со списком категорий.
    GET - получить все категории с количеством товаров
    POST - создать новую категорию
    """
    # Обработка GET запроса - получение списка всех категорий
    if request.method == 'GET':
        # annotate добавляет к каждой категории подсчет количества товаров
        categories = Category.objects.annotate(
            products_count=Count('products')  # Count считает связанные товары
        )
        data = CategoryListSerializers(categories, many=True).data  # many=True для списка объектов
        return Response(data, status=status.HTTP_200_OK)
    
    # Обработка POST запроса - создание новой категории
    elif request.method == 'POST':
        # Используем валидирующий сериализатор для проверки входных данных
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            # Если данные не валидны, возвращаем ошибки валидации
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем уже проверенные данные
        name = serializer.validated_data['name']

        # Используем транзакцию для безопасного создания объекта
        with transaction.atomic():
            category = Category.objects.create(name=name)
            category.save()  # Явно сохраняем объект
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializers(category).data)

@api_view(['GET', 'PUT', 'DELETE'])  # Работа с одним товаром
def product_detail(request, id):
    """
    Обработка конкретного товара по ID.
    GET - получить товар, PUT - обновить, DELETE - удалить
    """
    # Ищем товар по ID
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET - возврат информации о товаре
    if request.method == 'GET':
        data = ProductDetailSerializers(product).data
        return Response(data=data)
    
    # PUT - обновление товара
    elif request.method == 'PUT':
        # Получаем данные из запроса
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_data = request.data.get('category_id') or request.data.get('category')
        
        # Обновляем только переданные поля (частичное обновление)
        if title:
            product.title = title 
        if description:
            product.description = description
        if price:
            product.price = price
        if category_data:
            try:
                # Проверяем, передан ID категории или название
                if isinstance(category_data, int) or (isinstance(category_data, str) and category_data.isdigit()):
                    product.category_id = int(category_data)  # Устанавливаем по ID
                else:
                    category = Category.objects.get(name=category_data)  # Ищем по названию
                    product.category = category
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.save()  # Сохраняем изменения в базе данных
        data = ProductDetailSerializers(product).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    # DELETE - удаление товара
    elif request.method == 'DELETE':
        product.delete()  # Удаляем товар из базы данных
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])  # Список товаров и создание нового
def product_create_list(request):
    """
    Работа со списком товаров.
    GET - получить все товары
    POST - создать новый товар
    """
    # GET - получение списка всех товаров
    if request.method == 'GET':
        products = Product.objects.all()  # Получаем все товары
        data = ProductListSerializers(products, many=True).data  # Преобразуем в JSON
        return Response(data=data, status=status.HTTP_200_OK)
    
    # POST - создание нового товара
    elif request.method == 'POST':
        # Используем валидирующий сериализатор для проверки входных данных
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            # Возвращаем ошибки валидации, если данные некорректны
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Извлекаем уже проверенные данные из сериализатора
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        # Создаем товар в атомарной транзакции для безопасности
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category_id=category_id,
            )
        return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializers(product).data)
      # 201 = успешное создание

@api_view(['GET', 'PUT', 'DELETE'])  # Работа с одним отзывом
def review_detail(request, id):
    """
    Обработка конкретного отзыва по ID.
    GET - получить отзыв, PUT - обновить, DELETE - удалить
    """
    # Ищем отзыв по ID
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET - возврат информации об отзыве
    if request.method == 'GET':
        data = ReviewDetailSerializers(review).data
        return Response(data=data)
    
    # PUT - обновление отзыва
    elif request.method == 'PUT':
        # Получаем новые данные из запроса
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product')
        
        # Обновляем поля отзыва
        review.text = text
        review.stars = stars 
        review.product_id = product_id
        review.save()  # Сохраняем изменения
        data = ReviewDetailSerializers(review).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    # DELETE - удаление отзыва
    elif request.method == 'DELETE':
        review.delete()  # Удаляем отзыв из базы данных
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])  # Список отзывов и создание нового
def review_create_list(request):
    """
    Работа со списком отзывов.
    GET - получить все отзывы
    POST - создать новый отзыв
    """
    # GET - получение списка всех отзывов
    if request.method == 'GET':
        # select_related оптимизирует запросы, загружая связанные товары сразу
        reviews = Review.objects.select_related('product')
        data = ReviewListSerializers(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    # POST - создание нового отзыва
    elif request.method == 'POST':
        # Используем валидирующий сериализатор для проверки данных отзыва
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            # Возвращаем ошибки валидации (например, неправильный рейтинг)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Извлекаем проверенные данные
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')  # Рейтинг от 1 до 5
        product_id = serializer.validated_data.get('product_id')

        # Создаем отзыв в атомарной транзакции
        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                stars=stars,
                product_id=product_id,
            )
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializers(review).data)
    


@api_view(['GET'])  # Только чтение
def products_with_reviews(request):
    """
    Специальный эндпоинт /api/v1/products/reviews/
    Возвращает список всех товаров с их отзывами и средним рейтингом.
    Используется для отображения товаров с полной информацией об отзывах.
    """
    # prefetch_related оптимизирует загрузку связанных отзывов
    # annotate добавляет вычисляемое поле average_rating (средний рейтинг)
    products = Product.objects.prefetch_related('reviews').annotate(
        average_rating=Avg('reviews__stars')  # Avg вычисляет среднее значение звезд
    )
    data = ProductSerializer(products, many=True).data  # Используем специальный сериализатор
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])  # Только получение данных
def categories_with_count(request):
    """
    Альтернативный эндпоинт для категорий (устаревший).
    Возвращает список всех категорий с количеством товаров в каждой.
    Аналогичен category_create_list, но без возможности создания.
    """
    # annotate добавляет к каждой категории подсчет количества товаров
    categories = Category.objects.annotate(
        products_count=Count('products')  # Count считает связанные товары через ForeignKey
    )
    data = CategoryListSerializers(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)
   