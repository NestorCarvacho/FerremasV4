from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Order, Orderdetails, Customer, Cart
from ..serializers import OrderSerializer, OrderCreateSerializer, OrderDetailsSerializer

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get user's orders (customers see their own, employees see all)",
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        if request.user.user_type == 'customer':
            try:
                customer = request.user.customer
                orders = Order.objects.filter(customer=customer)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer profile not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        elif request.user.user_type == 'employee':
            orders = Order.objects.all()
        else:
            return Response({'error': 'Invalid user type'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get order details by ID",
        responses={
            200: OrderSerializer,
            404: openapi.Response(description="Order not found"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def get(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        
        # Check permissions
        if request.user.user_type == 'customer':
            try:
                customer = request.user.customer
                if order.customer != customer:
                    return Response({'error': 'Access denied'}, 
                                  status=status.HTTP_403_FORBIDDEN)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer profile not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
        elif request.user.user_type != 'employee':
            return Response({'error': 'Access denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Create new order from cart (Customer only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'required_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'freight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'shipper': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shipper ID'),
                'from_cart': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Create from cart items', default=True)
            }
        ),
        responses={
            201: OrderSerializer,
            400: openapi.Response(description="Bad request"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def post(self, request):
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can create orders'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            customer = request.user.customer
            
            # Create order from cart if requested
            if request.data.get('from_cart', True):
                cart_items = Cart.objects.filter(customer=customer)
                if not cart_items.exists():
                    return Response({'error': 'Cart is empty'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                # Create order
                order = Order.objects.create(
                    customer=customer,
                    order_date=timezone.now(),
                    required_date=request.data.get('required_date'),
                    freight=request.data.get('freight', 0),
                    shipper_id=request.data.get('shipper')
                )
                
                # Create order details from cart
                for cart_item in cart_items:
                    Orderdetails.objects.create(
                        order=order,
                        product=cart_item.product,
                        unit_price=cart_item.product.unit_price,
                        quantity=cart_item.num_of_products,
                        discount=cart_item.product.discount or 0
                    )
                
                # Clear cart
                cart_items.delete()
                
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            else:
                # Custom order creation logic can be added here
                serializer = OrderCreateSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    order = serializer.save()
                    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

class OrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update order status (Employee only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'shipped_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'freight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'shipper': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: OrderSerializer,
            404: openapi.Response(description="Order not found"),
            403: openapi.Response(description="Permission denied")
        }
    )
    def put(self, request, order_id):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can update orders'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        order = get_object_or_404(Order, order_id=order_id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
