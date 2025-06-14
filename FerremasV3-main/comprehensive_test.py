import requests
import json
import time

class EcommerceAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.customer_token = None
        self.created_ids = {
            'categories': [],
            'suppliers': [],
            'products': [],
            'carts': [],
            'orders': []
        }
    
    def login(self, username, password):
        """Login and get access token"""
        login_data = {"username": username, "password": password}
        response = requests.post(f'{self.base_url}/api/auth/login/', json=login_data)
        if response.status_code == 200:
            return response.json()['tokens']['access']
        else:
            print(f"Login failed for {username}: {response.text}")
            return None
    
    def test_authentication(self):
        """Test authentication endpoints"""
        print("\n=== TESTING AUTHENTICATION ===")
        
        # Login admin
        print("1. Testing admin login...")
        self.admin_token = self.login("admin", "admin123")
        if self.admin_token:
            print("✅ Admin login successful")
        else:
            print("❌ Admin login failed")
            return False
        
        # Login customer
        print("2. Testing customer login...")
        self.customer_token = self.login("testuser", "testpass123")
        if self.customer_token:
            print("✅ Customer login successful")
        else:
            print("❌ Customer login failed")
            return False
        
        # Test user profile
        print("3. Testing user profile...")
        headers = {'Authorization': f'Bearer {self.customer_token}'}
        response = requests.get(f'{self.base_url}/api/auth/profile/', headers=headers)
        if response.status_code == 200:
            print("✅ User profile retrieved successfully")
            print(f"   User: {response.json()['username']}")
        else:
            print(f"❌ User profile failed: {response.text}")
        
        return True
    
    def test_categories(self):
        """Test category endpoints"""
        print("\n=== TESTING CATEGORIES ===")
        
        headers = {'Authorization': f'Bearer {self.admin_token}', 'Content-Type': 'application/json'}
        
        # Create category
        print("1. Creating category...")
        category_data = {
            "category_name": "Test Electronics",
            "description": "Electronic devices for testing"
        }
        response = requests.post(f'{self.base_url}/api/categories/manage/', json=category_data, headers=headers)
        if response.status_code == 201:
            category_id = response.json()['category_id']
            self.created_ids['categories'].append(category_id)
            print(f"✅ Category created with ID: {category_id}")
        else:
            print(f"❌ Category creation failed: {response.text}")
            return False
        
        # List categories
        print("2. Listing categories...")
        response = requests.get(f'{self.base_url}/api/categories/')
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Found {len(categories)} categories")
        else:
            print(f"❌ Category listing failed: {response.text}")
        
        # Get category detail
        print("3. Getting category detail...")
        response = requests.get(f'{self.base_url}/api/categories/{category_id}/')
        if response.status_code == 200:
            print("✅ Category detail retrieved successfully")
        else:
            print(f"❌ Category detail failed: {response.text}")
        
        return True
    
    def test_suppliers(self):
        """Test supplier endpoints"""
        print("\n=== TESTING SUPPLIERS ===")
        
        headers = {'Authorization': f'Bearer {self.admin_token}', 'Content-Type': 'application/json'}
        
        # Create supplier
        print("1. Creating supplier...")
        supplier_data = {
            "company_name": "Test Supplier Co",
            "contact_name": "Test Contact",
            "address": "123 Test Street",
            "city": "Test City",
            "postal_code": "12345",
            "country": "Test Country"
        }
        response = requests.post(f'{self.base_url}/api/suppliers/manage/', json=supplier_data, headers=headers)
        if response.status_code == 201:
            supplier_id = response.json()['supplier_id']
            self.created_ids['suppliers'].append(supplier_id)
            print(f"✅ Supplier created with ID: {supplier_id}")
        else:
            print(f"❌ Supplier creation failed: {response.text}")
            return False
          # List suppliers
        print("2. Listing suppliers...")
        response = requests.get(f'{self.base_url}/api/suppliers/', headers=headers)
        if response.status_code == 200:
            suppliers = response.json()
            print(f"✅ Found {len(suppliers)} suppliers")
        else:
            print(f"❌ Supplier listing failed: {response.text}")
        
        return True
    
    def test_products(self):
        """Test product endpoints"""
        print("\n=== TESTING PRODUCTS ===")
        
        if not self.created_ids['categories'] or not self.created_ids['suppliers']:
            print("❌ Need categories and suppliers to test products")
            return False
        
        headers = {'Authorization': f'Bearer {self.admin_token}', 'Content-Type': 'application/json'}
        
        # Create product
        print("1. Creating product...")
        product_data = {
            "product_name": "Test Smartphone",
            "supplier": self.created_ids['suppliers'][0],
            "category": self.created_ids['categories'][0],
            "quantity_per_unit": "1 unit",
            "unit_price": "299.99",
            "units_in_stock": 50,
            "units_on_order": 0,
            "reorder_level": 10,
            "discontinued": False
        }
        response = requests.post(f'{self.base_url}/api/products/manage/', json=product_data, headers=headers)
        if response.status_code == 201:
            product_id = response.json()['product_id']
            self.created_ids['products'].append(product_id)
            print(f"✅ Product created with ID: {product_id}")
        else:
            print(f"❌ Product creation failed: {response.text}")
            return False
        
        # List products
        print("2. Listing products...")
        response = requests.get(f'{self.base_url}/api/products/')
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} products")
        else:
            print(f"❌ Product listing failed: {response.text}")
        
        # Test category products
        print("3. Testing category products...")
        category_id = self.created_ids['categories'][0]
        response = requests.get(f'{self.base_url}/api/categories/{category_id}/products/')
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} products in category")
        else:
            print(f"❌ Category products failed: {response.text}")
        
        return True
    
    def test_cart(self):
        """Test cart endpoints"""
        print("\n=== TESTING CART ===")
        
        if not self.created_ids['products']:
            print("❌ Need products to test cart")
            return False
        
        headers = {'Authorization': f'Bearer {self.customer_token}', 'Content-Type': 'application/json'}
        
        # Add item to cart
        print("1. Adding item to cart...")
        cart_data = {
            "product": self.created_ids['products'][0],
            "num_of_products": 2
        }
        response = requests.post(f'{self.base_url}/api/cart/', json=cart_data, headers=headers)
        if response.status_code == 201:
            cart_item = response.json()
            print(f"✅ Item added to cart: {cart_item}")
        else:
            print(f"❌ Cart add failed: {response.text}")
            return False
          # Get cart items
        print("2. Getting cart items...")
        response = requests.get(f'{self.base_url}/api/cart/', headers=headers)
        if response.status_code == 200:
            cart_items = response.json()
            print(f"✅ Found {len(cart_items)} items in cart")
            if cart_items:
                cart_id = cart_items[0]['id']  # Using 'id' instead of 'cart_id'
                self.created_ids['carts'].append(cart_id)
        else:
            print(f"❌ Cart get failed: {response.text}")
        
        return True
    
    def test_orders(self):
        """Test order endpoints"""
        print("\n=== TESTING ORDERS ===")
        
        headers = {'Authorization': f'Bearer {self.customer_token}', 'Content-Type': 'application/json'}
        
        # Create order
        print("1. Creating order...")
        order_data = {
            "shipping_address": "123 Test Address",
            "shipping_city": "Test City",
            "shipping_postal_code": "12345",
            "shipping_country": "Test Country"
        }
        response = requests.post(f'{self.base_url}/api/orders/create/', json=order_data, headers=headers)
        if response.status_code == 201:
            order = response.json()
            order_id = order['order_id']
            self.created_ids['orders'].append(order_id)
            print(f"✅ Order created with ID: {order_id}")
        else:
            print(f"❌ Order creation failed: {response.text}")
            return False
        
        # List orders
        print("2. Listing orders...")
        response = requests.get(f'{self.base_url}/api/orders/', headers=headers)
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Found {len(orders)} orders")
        else:
            print(f"❌ Order listing failed: {response.text}")
        
        # Get order detail
        print("3. Getting order detail...")
        if self.created_ids['orders']:
            order_id = self.created_ids['orders'][0]
            response = requests.get(f'{self.base_url}/api/orders/{order_id}/', headers=headers)
            if response.status_code == 200:
                print("✅ Order detail retrieved successfully")
            else:
                print(f"❌ Order detail failed: {response.text}")
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting comprehensive API tests...")
        
        # Test authentication first
        if not self.test_authentication():
            print("❌ Authentication tests failed - stopping")
            return
        
        # Test all endpoints
        self.test_categories()
        self.test_suppliers()
        self.test_products()
        self.test_cart()
        self.test_orders()
        
        print("\n=== TEST SUMMARY ===")
        print(f"Created categories: {len(self.created_ids['categories'])}")
        print(f"Created suppliers: {len(self.created_ids['suppliers'])}")
        print(f"Created products: {len(self.created_ids['products'])}")
        print(f"Created cart items: {len(self.created_ids['carts'])}")
        print(f"Created orders: {len(self.created_ids['orders'])}")
        print("✅ All tests completed!")

if __name__ == "__main__":
    tester = EcommerceAPITester()
    tester.run_all_tests()
