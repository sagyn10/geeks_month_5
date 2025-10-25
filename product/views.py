from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import (
    CategoryDetailSerializers, CategoryListSerializers,
    ProductDetailSerializers, ProductListSerializers,
    ReviewDetailSerializers, ReviewListSerializers,
)

@api_view(['GET'])
def catgory_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = CategoryDetailSerializers(category).data
    return Response(data=data) 

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    data = CategoryListSerializers(categories, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = ProductDetailSerializers(product).data
    return Response(data=data)

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    data = ProductListSerializers(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = ReviewDetailSerializers(review).data
    return Response(data=data)

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    data = ReviewListSerializers(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)
