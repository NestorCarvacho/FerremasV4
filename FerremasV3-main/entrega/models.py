from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'employee')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'auth_user'

class Billinginfo(models.Model):
    billing_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)
    credit_card_pin = models.CharField(max_length=4, blank=True, null=True)
    credit_card_exp_date = models.DateField(blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'BillingInfo'


class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    num_of_products = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Cart'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def create(cls, category_name=None, description=None, picture=None):
        if not category_name:
            category_name = "Default Category"
        category = cls(category_name=category_name, description=description, picture=picture)
        category.save()
        return category

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.category_name or "Unnamed Category"


class Customer(models.Model):
    user = models.OneToOneField('entrega.User', on_delete=models.CASCADE, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Customer'

    def __str__(self):
        return f"{self.contact_name} {self.last_name}" if self.contact_name else "Unnamed Customer"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    required_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipper = models.ForeignKey('Shipper', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f"Order #{self.order_id}"


class Orderdetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'OrderDetails'


class Personalinfo(models.Model):
    personal_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('entrega.User', on_delete=models.CASCADE, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'PersonalInfo'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    quantity_per_unit = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    units_in_order = models.IntegerField(blank=True, null=True)
    units_in_stock = models.IntegerField(blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Product'

    def __str__(self):
        return self.product_name or "Unnamed Product"


class Shipper(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'Shipper'

    def __str__(self):
        return self.company_name or "Unnamed Shipper"


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_title = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'Supplier'

    def __str__(self):
        return self.contact_name or "Unnamed Supplier"
