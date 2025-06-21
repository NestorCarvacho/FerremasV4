from django.test import TestCase
from entrega.models import Category

class CategoryModelTest(TestCase):

    def test_create_category_with_all_fields(self):
        category = Category.create(
            category_name="Bebidas",
            description="Bebidas frías y calientes",
            picture="images/drinks.jpg"
        )
        self.assertEqual(category.category_name, "Bebidas")
        self.assertEqual(category.description, "Bebidas frías y calientes")
        self.assertEqual(category.picture, "images/drinks.jpg")

    def test_create_category_with_optional_fields_blank(self):
        category = Category.create()
        self.assertEqual(category.category_name, "Default Category")
        self.assertIsNone(category.description)
        self.assertIsNone(category.picture)

    def test_category_str_with_name(self):
        category = Category.objects.create(category_name="Snacks")
        self.assertEqual(str(category), "Snacks")

    def test_category_str_without_name(self):
        category = Category.objects.create()
        self.assertEqual(str(category), "Unnamed Category")

    def test_max_length_category_name(self):
        name = "A" * 100
        category = Category.objects.create(category_name=name)
        self.assertEqual(category.category_name, name)

    def test_max_length_picture_field(self):
        picture_path = "a" * 255
        category = Category.objects.create(picture=picture_path)
        self.assertEqual(category.picture, picture_path)