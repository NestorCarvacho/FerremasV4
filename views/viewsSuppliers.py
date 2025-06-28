from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Supplier, Product
from ..serializers import SupplierSerializer, ProductSerializer

class SupplierListView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users
    
    @swagger_auto_schema(
        operation_description="Get all suppliers",
        responses={200: SupplierSerializer(many=True)}
    )
    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

class SupplierDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get supplier by ID",
        responses={
            200: SupplierSerializer,
            404: openapi.Response(description="Supplier not found")
        }
    )
    def get(self, request, supplier_id):
        supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

class SupplierProductsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get all products from a specific supplier",
        responses={
            200: ProductSerializer(many=True),
            404: openapi.Response(description="Supplier not found")
        }
    )
    def get(self, request, supplier_id):
        supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
        products = Product.objects.filter(supplier=supplier)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class SupplierManagementView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Create new supplier (Employee only)",
        request_body=SupplierSerializer,
        responses={
            201: SupplierSerializer,
            403: openapi.Response(description="Permission denied"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can create suppliers'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update supplier (Employee only)",
        request_body=SupplierSerializer,
        responses={
            200: SupplierSerializer,
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Supplier not found")
        }
    )
    def put(self, request, supplier_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can update suppliers'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete supplier (Employee only)",
        responses={
            204: openapi.Response(description="Supplier deleted successfully"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Supplier not found")
        }
    )
    def delete(self, request, supplier_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can delete suppliers'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
        supplier.delete()
        return Response({'message': 'Supplier deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
