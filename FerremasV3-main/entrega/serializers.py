from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import *

# User Registration and Authentication Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'user_type')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Create Customer or Supplier profile based on user_type
        if user.user_type == 'customer':
            Customer.objects.create(
                user=user,
                contact_name=user.first_name,
                last_name=user.last_name
            )
        elif user.user_type == 'employee':
            Supplier.objects.create(
                user=user,
                contact_name=user.first_name
            )
        
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'date_joined')
        read_only_fields = ('id', 'date_joined')

# Category Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Product Serializers
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.contact_name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Customer Serializers
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

# Supplier Serializers
class SupplierSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Supplier
        fields = '__all__'

# Cart Serializers
class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_price = serializers.DecimalField(source='product.unit_price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('product', 'num_of_products')
    
    def create(self, validated_data):
        customer = self.context['request'].user.customer
        product = validated_data['product']
        num_of_products = validated_data['num_of_products']
        
        # Calculate total price
        total_price = product.unit_price * num_of_products
        
        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            customer=customer,
            product=product,
            defaults={
                'num_of_products': num_of_products,
                'total_price': total_price
            }
        )
        
        if not created:
            # Update existing cart item
            cart_item.num_of_products += num_of_products
            cart_item.total_price = cart_item.product.unit_price * cart_item.num_of_products
            cart_item.save()
        
        return cart_item

# Order Serializers
class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = Orderdetails
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(source='orderdetails_set', many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.contact_name', read_only=True)
    shipper_name = serializers.CharField(source='shipper.company_name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    order_details = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Order
        fields = ('required_date', 'freight', 'shipper', 'order_details')
    
    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        customer = self.context['request'].user.customer
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            order_date=timezone.now(),
            **validated_data
        )
        
        # Create order details
        for detail_data in order_details_data:
            Orderdetails.objects.create(
                order=order,
                **detail_data
            )
        
        return order

# Billing Info Serializers
class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billinginfo
        fields = '__all__'

# Shipper Serializers
class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipper
        fields = '__all__'

# Personal Info Serializers
class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalinfo
        fields = '__all__'
