from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Category, Product
from ..serializers import CategorySerializer, ProductSerializer

class CategoryListView(APIView):
    permission_classes = [AllowAny]  # Anyone can view categories
    
    @swagger_auto_schema(
        operation_description="Get all categories",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):
    permission_classes = [AllowAny]  # Anyone can view categories
    
    @swagger_auto_schema(
        operation_description="Get category by ID",
        responses={
            200: CategorySerializer,
            404: openapi.Response(description="Category not found")
        }
    )
    def get(self, request, category_id):
        category = get_object_or_404(Category, category_id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class CategoryProductsView(APIView):
    permission_classes = [AllowAny]  # Anyone can view products
    
    @swagger_auto_schema(
        operation_description="Get all products in a specific category",
        responses={
            200: ProductSerializer(many=True),
            404: openapi.Response(description="Category not found")
        }
    )
    def get(self, request, category_id):
        category = get_object_or_404(Category, category_id=category_id)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryManagementView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can manage
    
    @swagger_auto_schema(
        operation_description="Create a new category (Employee only)",
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
            403: openapi.Response(description="Permission denied"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        # Only employees can create categories
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can create categories'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update category (Employee only)",
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer,
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Category not found")
        }
    )
    def put(self, request, category_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can update categories'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        category = get_object_or_404(Category, category_id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete category (Employee only)",
        responses={
            204: openapi.Response(description="Category deleted successfully"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Category not found")
        }
    )
    def delete(self, request, category_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can delete categories'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        category = get_object_or_404(Category, category_id=category_id)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
