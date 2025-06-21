from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from entrega.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()

class CategoryIntegrationTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_superuser(username="testuser", password="testpassword")

        # Obtener el token de acceso
        response = self.client.post(
            reverse('token_obtain_pair'), 
            {'username': 'testuser', 'password': 'testpassword'},
            content_type='application/json'
        )
        self.access_token = response.json().get('access')

    def test_create_category_integration(self):
        # Verificar que no hay categorías antes de la prueba
        self.assertEqual(Category.objects.count(), 0)

        # Datos para crear una nueva categoría
        data = {
            'category_name': 'Electrónica',
            'description': 'Categoría de productos electrónicos'
        }

        # Realizar una petición POST al endpoint de creación de categoría
        response = self.client.post(reverse('category_create'), data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}',content_type='application/json')

        # Verificar que el código de estado sea 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que se devuelve la lista de categorías
        self.assertEqual(len(response.json()), 4)
        new_category = response.json()
        print("esta es la cattgoria nueva",new_category)
        self.assertEqual(new_category['category_name'], 'Electrónica')
        self.assertEqual(new_category['description'], 'Categoría de productos electrónicos')

    def test_category_list_view(self):
        # Crear algunas categorías
        Category.objects.create(category_name="Electrónica", description="Productos electrónicos")
        Category.objects.create(category_name="Muebles", description="Muebles de oficina")

        # Hacer una petición GET al endpoint de lista de categorías
        response = self.client.get(reverse('category_list'), content_type='application/json')

        # Verificar que el código de estado sea 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que se devuelve la lista de categorías
        self.assertEqual(len(response.json()), 2)  # 2 categorías creadas