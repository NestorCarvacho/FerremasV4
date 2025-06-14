from django.core.management.base import BaseCommand
from entrega.models import Category, Supplier, Product, User, Customer
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'category_name': 'Electronics', 'description': 'Electronic devices and accessories'},
            {'category_name': 'Tools', 'description': 'Hand tools and power tools'},
            {'category_name': 'Hardware', 'description': 'Screws, bolts, and hardware'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                category_name=cat_data['category_name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.category_name}')

        # Create suppliers
        suppliers_data = [
            {'company_name': 'Tech Supplies Co', 'contact_name': 'John Smith', 'phone': '555-0101'},
            {'company_name': 'Hardware Plus', 'contact_name': 'Jane Doe', 'phone': '555-0102'},
        ]
        
        for sup_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                company_name=sup_data['company_name'],
                defaults=sup_data
            )
            if created:
                self.stdout.write(f'Created supplier: {supplier.company_name}')

        # Create products
        products_data = [
            {
                'product_name': 'Wireless Headphones',
                'unit_price': Decimal('99.99'),
                'units_in_stock': 50,
                'category': Category.objects.get(category_name='Electronics'),
                'supplier': Supplier.objects.get(company_name='Tech Supplies Co'),
            },
            {
                'product_name': 'Power Drill',
                'unit_price': Decimal('149.99'),
                'units_in_stock': 25,
                'category': Category.objects.get(category_name='Tools'),
                'supplier': Supplier.objects.get(company_name='Hardware Plus'),
            },
            {
                'product_name': 'Bluetooth Speaker',
                'unit_price': Decimal('79.99'),
                'units_in_stock': 30,
                'category': Category.objects.get(category_name='Electronics'),
                'supplier': Supplier.objects.get(company_name='Tech Supplies Co'),
            },
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                product_name=prod_data['product_name'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.product_name}')

        # Create test customer user
        customer_user, created = User.objects.get_or_create(
            username='testcustomer',
            defaults={
                'email': 'customer@test.com',
                'user_type': 'customer',
                'first_name': 'Test',
                'last_name': 'Customer'
            }
        )
        if created:
            customer_user.set_password('testpass123')
            customer_user.save()
            
            # Create customer profile
            Customer.objects.get_or_create(
                user=customer_user,
                defaults={
                    'company_name': 'Test Customer Co',
                    'contact_name': 'Test Customer',
                    'phone': '555-0001'
                }
            )
            self.stdout.write('Created test customer user and profile')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
