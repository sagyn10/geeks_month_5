from rest_framework import serializers
from .models import Product, Category, Review
from django.db.models import Avg, Count



class ReviewSerializer(serializers.ModelSerializer):
    """Простой сериализатор для отзывов в эндпоинте /api/v1/products/reviews/"""
    class Meta:
        model = Review
        fields = ['text', 'stars']


class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializers(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']
        

class CategoryDetailSerializers(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class CategoryListSerializers(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта /api/v1/products/reviews/"""
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.DecimalField(
        max_digits=3, decimal_places=1, read_only=True, 
        source='average_rating'
    )
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'rating', 'reviews']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializers(many=True, read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )
    category = CategoryDetailSerializers(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 
                 'created_at', 'updated_at', 'reviews', 'average_rating']
        # depth = 1

class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price']

