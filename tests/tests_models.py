from django.test import TestCase
from entrega.models import Category, Product, Supplier

class CategoryModelTest(TestCase):
    # Prueba que se puede crear una categoría con el campo obligatorio category_name
    def test_create_category_with_required_fields(self):
        category = Category.objects.create(category_name="Herramientas")
        self.assertEqual(category.category_name, "Herramientas")
        print("Unitaria -  Prueba que se puede crear una categoría con el campo obligatorio category_name")

    # Prueba que los campos no pueden quedar en blanco y sean None si no se especifican
    def test_category_blank_fields(self):
        category = Category.objects.create()
        self.assertEqual(category.category_name, "")
        self.assertIsNone(category.description)
        self.assertIsNone(category.picture)
        print("Unitaria -  Prueba que los campos no pueden quedar en blanco y sean None si no se especifican")

    # Prueba el método __str__ cuando category_name tiene valor
    def test_category_str_method(self):
        category = Category.objects.create(category_name="Clavos")
        self.assertEqual(str(category), "Clavos")
        print("Unitaria -  Prueba el método __str__ cuando category_name tiene valor")

    # Prueba el método __str__ cuando category_name es None
    def test_category_str_method_without_name(self):
        category = Category.objects.create()
        self.assertEqual(str(category), "Unnamed Category")
        print("Unitaria -  Prueba el método __str__ cuando category_name es None")

class ProductModelTest(TestCase):
    def setUp(self):
        # Crea una categoría para usarla como ForeignKey en los productos
        self.category = Category.objects.create(category_name="Electricidad")
        print("Unitaria -  Crea una categoría para usarla como ForeignKey en los productos")

    # Prueba que se puede crear un producto con los campos obligatorios
    def test_create_product_with_required_fields(self):
        product = Product.objects.create(
            product_name="Cable",
            category=self.category,
            unit_price=1000
        )
        self.assertEqual(product.product_name, "Cable")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.unit_price, 1000)
        print("Unitaria -  Prueba que se puede crear un producto con los campos obligatorios")

    # Prueba que los campos opcionales de Product pueden quedar en blanco y sean None
    def test_product_blank_fields(self):
        product = Product.objects.create()
        self.assertIsNone(product.product_name)
        self.assertIsNone(product.category)
        self.assertIsNone(product.unit_price)
        self.assertIsNone(product.supplier)
        self.assertIsNone(product.quantity_per_unit)
        self.assertIsNone(product.units_in_order)
        self.assertIsNone(product.units_in_stock)
        self.assertIsNone(product.reorder_level)
        self.assertIsNone(product.discount)
        self.assertIsNone(product.picture)
        print("Unitaria -  Prueba que los campos opcionales de Product pueden quedar en blanco y sean None")

    # Prueba el método __str__ cuando product_name tiene valor
    def test_product_str_method(self):
        product = Product.objects.create(product_name="Enchufe")
        self.assertEqual(str(product), "Enchufe")
        print("Unitaria -  Prueba el método __str__ cuando product_name tiene valor")

    # Prueba el método __str__ cuando product_name es None
    def test_product_str_method_without_name(self):
        product = Product.objects.create()
        self.assertEqual(str(product), "Unnamed Product")
        print("Unitaria -  Prueba el método __str__ cuando product_name es None")

class SupplierModelTest(TestCase):
    # Prueba que los campos opcionales de Supplier pueden quedar en blanco y sean None
    def test_create_supplier_with_blank_fields(self):
        supplier = Supplier.objects.create()
        self.assertIsNone(supplier.contact_name)
        self.assertIsNone(supplier.contact_title)
        self.assertIsNone(supplier.address)
        self.assertIsNone(supplier.phone)
        self.assertIsNone(supplier.user)
        print("Unitaria -  Prueba que los campos opcionales de Supplier pueden quedar en blanco y sean None")

    # Prueba el método __str__ cuando contact_name tiene valor
    def test_supplier_str_method(self):
        supplier = Supplier.objects.create(contact_name="Proveedor Dos")
        self.assertEqual(str(supplier), "Proveedor Dos")
        print("Unitaria -  Prueba el método __str__ cuando contact_name tiene valor")

    # Prueba el método __str__ cuando contact_name es None
    def test_supplier_str_method_without_name(self):
        supplier = Supplier.objects.create()
        self.assertEqual(str(supplier), "Unnamed Supplier")
        print("Unitaria -  Prueba el método __str__ cuando contact_name es None")