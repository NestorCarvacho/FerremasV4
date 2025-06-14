from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Product, Category, Supplier
from ..serializers import ProductSerializer, ProductCreateSerializer

class ProductListView(APIView):
    permission_classes = [AllowAny]  # Anyone can view products
    
    @swagger_auto_schema(
        operation_description="Get all products with optional filtering",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in product name", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        products = Product.objects.all()
        
        # Apply filters
        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(product_name__icontains=search) | 
                Q(category__category_name__icontains=search)
            )
        
        category_id = request.GET.get('category')
        if category_id:
            products = products.filter(category_id=category_id)
        
        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(unit_price__gte=min_price)
        
        max_price = request.GET.get('max_price')
        if max_price:
            products = products.filter(unit_price__lte=max_price)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [AllowAny]  # Anyone can view product details
    
    @swagger_auto_schema(
        operation_description="Get product by ID",
        responses={
            200: ProductSerializer,
            404: openapi.Response(description="Product not found")
        }
    )
    def get(self, request, product_id):
        product = get_object_or_404(Product, product_id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductManagementView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can manage
    
    @swagger_auto_schema(
        operation_description="Create a new product (Employee only)",
        request_body=ProductCreateSerializer,
        responses={
            201: ProductSerializer,
            403: openapi.Response(description="Permission denied"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        # Only employees can create products
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can create products'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update product (Employee only)",
        request_body=ProductCreateSerializer,
        responses={
            200: ProductSerializer,
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Product not found")
        }
    )
    def put(self, request, product_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can update products'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        product = get_object_or_404(Product, product_id=product_id)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            updated_product = serializer.save()
            return Response(ProductSerializer(updated_product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete product (Employee only)",
        responses={
            204: openapi.Response(description="Product deleted successfully"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Product not found")
        }
    )
    def delete(self, request, product_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can delete products'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        product = get_object_or_404(Product, product_id=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    