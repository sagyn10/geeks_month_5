from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from .models import Product, Category, Review
from .serializers import (
    CategoryDetailSerializers, CategoryListSerializers,
    ProductDetailSerializers, ProductListSerializers,
    ReviewDetailSerializers, ReviewListSerializers,
    ProductWithReviewsSerializer, ProductSerializer
)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializers(category).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        name = request.data.get('name')
        category.name = name
        category.save()
        data = CategoryDetailSerializers(category).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def category_create_list(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(
            products_count=Count('products')
        )
        data = CategoryListSerializers(categories, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(name=name)
        data = CategoryDetailSerializers(category).data
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializers(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_data = request.data.get('category_id') or request.data.get('category')
        
        if title:
            product.title = title 
        if description:
            product.description = description
        if price:
            product.price = price
        if category_data:
            try:
                if isinstance(category_data, int) or (isinstance(category_data, str) and category_data.isdigit()):
                    product.category_id = int(category_data)
                else:
                    category = Category.objects.get(name=category_data)
                    product.category = category
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.save()
        data = ProductDetailSerializers(product).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_create_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializers(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_data = request.data.get('category')

        # Поддержка как ID, так и названия категории
        try:
            if isinstance(category_data, int) or (isinstance(category_data, str) and category_data.isdigit()):
                # Если передан ID категории
                category = Category.objects.get(id=int(category_data))
            else:
                # Если передано название категории
                category = Category.objects.get(name=category_data)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category=category
        )
        data = ProductDetailSerializers(product).data
        return Response(data=data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializers(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product')
        review.text = text
        review.stars = stars 
        review.product_id = product_id
        review.save()
        data = ReviewDetailSerializers(review).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_create_list(request):
    if request.method == 'GET':
        reviews = Review.objects.select_related('product')
        data = ReviewListSerializers(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product')
        
        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )
        data = ReviewDetailSerializers(review).data
        return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def products_with_reviews(request):
    """
    Эндпоинт /api/v1/products/reviews/
    Возвращает список всех товаров с отзывами и средним рейтингом
    """
    products = Product.objects.prefetch_related('reviews').annotate(
        average_rating=Avg('reviews__stars')
    )
    data = ProductSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def categories_with_count(request):
    """
    Эндпоинт /api/v1/categories/
    Возвращает список всех категорий с количеством товаров
    """
    categories = Category.objects.annotate(
        products_count=Count('products')
    )
    data = CategoryListSerializers(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)
   