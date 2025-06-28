from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from entrega.models import Category, Product, Supplier, Customer
from django.contrib.auth import get_user_model
User = get_user_model()

class CategoryIntegrationTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba y obtener token JWT
        self.user = User.objects.create_superuser(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            content_type='application/json'
        )
        self.access_token = response.json().get('access')

    def test_create_category_integration(self):
        # Prueba la creación de una categoría vía API
        self.assertEqual(Category.objects.count(), 0)
        data = {
            'category_name': 'Electrónica',
            'description': 'Categoría de productos electrónicos'
        }
        response = self.client.post(
            reverse('category_create'), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = response.json()
        self.assertEqual(new_category['category_name'], 'Electrónica')
        self.assertEqual(new_category['description'], 'Categoría de productos electrónicos')
        print("Integracion - Prueba la creación de una categoría vía API")

    def test_category_list_view(self):
        # Prueba la obtención de la lista de categorías vía API
        Category.objects.create(category_name="Electrónica", description="Productos electrónicos")
        Category.objects.create(category_name="Muebles", description="Muebles de oficina")
        response = self.client.get(reverse('category_list'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        print("Integracion - Prueba la obtención de la lista de categorías vía API")

    def test_category_detail_view(self):
        # Prueba la obtención del detalle de una categoría
        category = Category.objects.create(category_name="Herramientas", description="Herramientas varias")
        response = self.client.get(reverse('category_detail', args=[category.pk]), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['category_name'], "Herramientas")
        print("Integracion - Prueba la obtención del detalle de una categoría")

    def test_update_category(self):
        # Prueba la actualización de una categoría vía API
        category = Category.objects.create(category_name="Antigua", description="Vieja desc")
        data = {'category_name': 'Nueva', 'description': 'Nueva desc'}
        response = self.client.put(
            reverse('category_update_delete', args=[category.pk]), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['category_name'], 'Nueva')
        print("Integracion - Prueba la actualización de una categoría vía API")

    def test_delete_category(self):
        # Prueba el borrado de una categoría vía API
        category = Category.objects.create(category_name="Eliminar", description="Borrar")
        response = self.client.delete(
            reverse('category_update_delete', args=[category.pk]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
        print("Integracion - Prueba el borrado de una categoría vía API")

    def test_create_category_without_auth(self):
        # Prueba que no se puede crear una categoría sin autenticación
        data = {'category_name': 'SinAuth', 'description': 'No autorizado'}
        response = self.client.post(reverse('category_create'), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Integracion - Prueba que no se puede crear una categoría sin autenticación")

    def test_update_category_without_auth(self):
        # Prueba que no se puede actualizar una categoría sin autenticación
        category = Category.objects.create(category_name="Vieja", description="Vieja desc")
        data = {'category_name': 'Intento', 'description': 'Sin token'}
        response = self.client.put(
            reverse('category_update_delete', args=[category.pk]), data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Integracion - Prueba que no se puede actualizar una categoría sin autenticación")

    def test_delete_category_without_auth(self):
        # Prueba que no se puede borrar una categoría sin autenticación
        category = Category.objects.create(category_name="Vieja", description="Vieja desc")
        response = self.client.delete(
            reverse('category_update_delete', args=[category.pk]),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Integracion - Prueba que no se puede borrar una categoría sin autenticación")

    def test_create_category_missing_fields(self):
        # Prueba que no se puede crear una categoría sin campos obligatorios
        data = {'description': 'Falta nombre'}
        response = self.client.post(
            reverse('category_create'), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Integracion - Prueba que no se puede crear una categoría sin campos obligatorios")

class ProductIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            content_type='application/json'
        )
        self.access_token = response.json().get('access')
        self.category = Category.objects.create(category_name="Herramientas")
        print("Integracion - Crear usuario y categoría para productos")

    def test_create_product(self):
        data = {'product_name': 'Martillo', 'category': self.category.pk, 'unit_price': 5000}
        response = self.client.post(
            reverse('product_create'), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Integracion - Prueba la creación de un producto vía API")

    def test_list_products(self):
        Product.objects.create(product_name="Martillo", category=self.category, unit_price=5000)
        response = self.client.get(reverse('product_list'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la obtención de la lista de productos vía API")

    def test_update_product(self):
        product = Product.objects.create(product_name="Destornillador", category=self.category, unit_price=2000)
        data = {'product_name': 'Destornillador Philips', 'category': self.category.pk, 'unit_price': 2500}
        response = self.client.put(
            reverse('product_update_delete', args=[product.pk]), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la actualización de un producto vía API")

    def test_delete_product(self):
        product = Product.objects.create(product_name="Taladro", category=self.category, unit_price=15000)
        response = self.client.delete(
            reverse('product_update_delete', args=[product.pk]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Integracion - Prueba el borrado de un producto vía API")

class SupplierIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            content_type='application/json'
        )
        self.access_token = response.json().get('access')
        print("Integracion - Crear usuario para proveedores")

    def test_create_supplier(self):
        data = {'contact_name': 'Proveedor Uno'}
        response = self.client.post(
            reverse('supplier_create'), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Integracion - Prueba la creación de un proveedor vía API")

    def test_list_suppliers(self):
        Supplier.objects.create(contact_name="Proveedor Uno")
        response = self.client.get(
            reverse('supplier_list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la obtención de la lista de proveedores vía API")

    def test_update_supplier(self):
        supplier = Supplier.objects.create(contact_name="Proveedor Dos")
        data = {'contact_name': 'Proveedor Dos Editado'}
        response = self.client.put(
            reverse('supplier_update_delete', args=[supplier.pk]), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la actualización de un proveedor vía API")

    def test_delete_supplier(self):
        supplier = Supplier.objects.create(contact_name="Proveedor Tres")
        response = self.client.delete(
            reverse('supplier_update_delete', args=[supplier.pk]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Integracion - Prueba el borrado de un proveedor vía API")

class OrderIntegrationTest(TestCase):
    def setUp(self):
        # Crea un usuario tipo customer
        self.user = User.objects.create_user(
            username="testcustomer",
            password="testpassword",
            user_type="customer"
        )
        # Crea el perfil Customer asociado (agrega otros campos obligatorios si existen)
        Customer.objects.create(user=self.user)
        # Obtén el token JWT
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testcustomer', 'password': 'testpassword'},
            content_type='application/json'
        )
        self.access_token = response.json().get('access')
        print("Integracion - Crear usuario y perfil Customer para órdenes")

    def test_create_order(self):
        # Crear categoría y producto
        from entrega.models import Category, Product, Cart, Customer
        category = Category.objects.create(category_name="Herramientas")
        product = Product.objects.create(product_name="Martillo", category=category, unit_price=5000)
        # Obtener el perfil Customer del usuario
        customer = Customer.objects.get(user=self.user)
        # Agregar producto al carrito
        Cart.objects.create(customer=customer, product=product, num_of_products=2, total_price=10000)
        # Intentar crear la orden (from_cart=True por defecto)
        data = {'order_date': '2024-06-27'}
        response = self.client.post(
            reverse('order_create'), data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Integracion - Prueba la creación de una orden vía API (con producto en carrito)")

    def test_list_orders(self):
        response = self.client.get(
            reverse('order_list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la obtención de la lista de órdenes vía API")

    def test_update_order(self):
        from entrega.models import Order
        from django.utils import timezone
        import datetime
        # Crear usuario tipo empleado y obtener token
        employee = User.objects.create_user(username="testemployee", password="testpassword", user_type="employee")
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testemployee', 'password': 'testpassword'},
            content_type='application/json'
        )
        employee_token = response.json().get('access')
        aware_date = timezone.make_aware(datetime.datetime(2024, 6, 27))
        order = Order.objects.create(order_date=aware_date)
        data = {'order_date': '2024-07-01'}
        response = self.client.put(
            reverse('order_update', args=[order.pk]), data,
            HTTP_AUTHORIZATION=f'Bearer {employee_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Integracion - Prueba la actualización de una orden vía API (con usuario empleado)")

    def test_delete_order(self):
        from entrega.models import Order
        from django.utils import timezone
        import datetime
        # Crear usuario tipo empleado y obtener token
        employee = User.objects.create_user(username="testemployee2", password="testpassword", user_type="employee")
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testemployee2', 'password': 'testpassword'},
            content_type='application/json'
        )
        employee_token = response.json().get('access')
        aware_date = timezone.make_aware(datetime.datetime(2024, 6, 27))
        order = Order.objects.create(order_date=aware_date)
        response = self.client.delete(
            reverse('order_update', args=[order.pk]),
            HTTP_AUTHORIZATION=f'Bearer {employee_token}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Integracion - Prueba el borrado de una orden vía API (con usuario empleado)")