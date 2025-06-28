from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Cart, Product, Customer
from ..serializers import CartSerializer, CartCreateSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get current user's cart items",
        responses={200: CartSerializer(many=True)}
    )
    def get(self, request):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers have cart access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            cart_items = Cart.objects.filter(customer=customer)
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Add item to cart",
        request_body=CartCreateSerializer,
        responses={
            201: CartSerializer,
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def post(self, request):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can add items to cart'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            serializer = CartCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                cart_item = serializer.save()
                return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update cart item quantity",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'num_of_products': openapi.Schema(type=openapi.TYPE_INTEGER, description='New quantity')
            },
            required=['num_of_products']
        ),
        responses={
            200: CartSerializer,
            404: openapi.Response(description="Cart item not found"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def put(self, request, cart_id):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can modify cart'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            cart_item = get_object_or_404(Cart, id=cart_id, customer=customer)
            
            new_quantity = request.data.get('num_of_products')
            if new_quantity and new_quantity > 0:
                cart_item.num_of_products = new_quantity
                cart_item.total_price = cart_item.product.unit_price * new_quantity
                cart_item.save()
                return Response(CartSerializer(cart_item).data)
            else:
                return Response({'error': 'Quantity must be greater than 0'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Remove item from cart",
        responses={
            204: openapi.Response(description="Item removed successfully"),
            404: openapi.Response(description="Cart item not found"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def delete(self, request, cart_id):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can modify cart'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            cart_item = get_object_or_404(Cart, id=cart_id, customer=customer)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, 
                           status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

class CartClearView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Clear all items from cart",
        responses={
            204: openapi.Response(description="Cart cleared successfully"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def delete(self, request):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can clear cart'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            Cart.objects.filter(customer=customer).delete()
            return Response({'message': 'Cart cleared successfully'}, 
                           status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
