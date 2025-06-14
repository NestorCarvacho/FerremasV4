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
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting comprehensive API tests...")
        
        # Test authentication first
        if not self.test_authentication():
            print("❌ Authentication tests failed - stopping")
            return
        
        print("✅ All basic tests completed!")

if __name__ == "__main__":
    tester = EcommerceAPITester()
    tester.run_all_tests()
    "username": "testuser",
    "password": "testpass123" 
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    print(f"Customer Login: {response.status_code}")
    if response.status_code == 200:
        tokens = response.json()['tokens']
        print("✅ Customer login successful")
        return tokens['access']
    else:
        print(f"❌ Customer login failed: {response.text}")
        return None

def test_admin_login():
    """Test admin login"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    print(f"Admin Login: {response.status_code}")
    if response.status_code == 200:
        tokens = response.json()['tokens']
        print("✅ Admin login successful")
        return tokens['access']
    else:
        print(f"❌ Admin login failed: {response.text}")
        return None

def test_cart_operations(customer_token):
    """Test cart CRUD operations"""
    print("\n=== Testing Cart Operations ===")
    
    headers = {
        'Authorization': f'Bearer {customer_token}',
        'Content-Type': 'application/json'
    }
    
    # Get cart items
    response = requests.get(f'{BASE_URL}/cart/', headers=headers)
    print(f"Get Cart: {response.status_code}")
    if response.status_code == 200:
        print("✅ Cart retrieval successful")
        cart_items = response.json()
        print(f"Current cart items: {len(cart_items)}")
    
    # Add item to cart
    cart_data = {
        "product": 1,
        "num_of_products": 3
    }
    
    response = requests.post(f'{BASE_URL}/cart/', json=cart_data, headers=headers)
    print(f"Add to Cart: {response.status_code}")
    if response.status_code == 201:
        print("✅ Add to cart successful")
        cart_item = response.json()
        cart_item_id = cart_item['id']
        print(f"Added cart item ID: {cart_item_id}")
        
        # Update cart item
        update_data = {"num_of_products": 5}
        response = requests.put(f'{BASE_URL}/cart/{cart_item_id}/', json=update_data, headers=headers)
        print(f"Update Cart Item: {response.status_code}")
        if response.status_code == 200:
            print("✅ Cart item update successful")
        
        # Delete cart item
        response = requests.delete(f'{BASE_URL}/cart/{cart_item_id}/', headers=headers)
        print(f"Delete Cart Item: {response.status_code}")
        if response.status_code == 204:
            print("✅ Cart item deletion successful")
    else:
        print(f"❌ Add to cart failed: {response.text}")

def test_order_operations(customer_token, admin_token):
    """Test order management"""
    print("\n=== Testing Order Operations ===")
    
    customer_headers = {
        'Authorization': f'Bearer {customer_token}',
        'Content-Type': 'application/json'
    }
    
    admin_headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    # First add item to cart
    cart_data = {
        "product": 1,
        "num_of_products": 2
    }
    requests.post(f'{BASE_URL}/cart/', json=cart_data, headers=customer_headers)
    
    # Create order from cart
    order_data = {
        "shipping_address": "123 Test Street, Test City",
        "payment_method": "credit_card"
    }
    
    response = requests.post(f'{BASE_URL}/orders/', json=order_data, headers=customer_headers)
    print(f"Create Order: {response.status_code}")
    if response.status_code == 201:
        print("✅ Order creation successful")
        order = response.json()
        order_id = order['id']
        print(f"Created order ID: {order_id}")
        
        # Get customer orders
        response = requests.get(f'{BASE_URL}/orders/', headers=customer_headers)
        print(f"Get Customer Orders: {response.status_code}")
        if response.status_code == 200:
            print("✅ Get customer orders successful")
        
        # Admin: Get all orders
        response = requests.get(f'{BASE_URL}/orders/manage/', headers=admin_headers)
        print(f"Admin Get All Orders: {response.status_code}")
        if response.status_code == 200:
            print("✅ Admin get all orders successful")
        
        # Admin: Update order status
        status_data = {"order_status": "shipped"}
        response = requests.put(f'{BASE_URL}/orders/manage/{order_id}/', json=status_data, headers=admin_headers)
        print(f"Update Order Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Order status update successful")
    else:
        print(f"❌ Order creation failed: {response.text}")

def test_product_operations(admin_token):
    """Test product management"""
    print("\n=== Testing Product Operations ===")
    
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    # Get all products
    response = requests.get(f'{BASE_URL}/products/')
    print(f"Get All Products: {response.status_code}")
    if response.status_code == 200:
        print("✅ Get products successful")
        products = response.json()
        print(f"Total products: {len(products)}")
    
    # Create new product
    product_data = {
        "product_name": "Test Product API",
        "description": "A test product created via API",
        "unit_price": "49.99",
        "stock_quantity": 100,
        "category": 1,
        "supplier": 1
    }
    
    response = requests.post(f'{BASE_URL}/products/manage/', json=product_data, headers=headers)
    print(f"Create Product: {response.status_code}")
    if response.status_code == 201:
        print("✅ Product creation successful")
        product = response.json()
        product_id = product['id']
        print(f"Created product ID: {product_id}")
        
        # Update product
        update_data = {
            "product_name": "Updated Test Product",
            "unit_price": "59.99"
        }
        response = requests.patch(f'{BASE_URL}/products/manage/{product_id}/', json=update_data, headers=headers)
        print(f"Update Product: {response.status_code}")
        if response.status_code == 200:
            print("✅ Product update successful")
        
        # Get single product
        response = requests.get(f'{BASE_URL}/products/{product_id}/')
        print(f"Get Single Product: {response.status_code}")
        if response.status_code == 200:
            print("✅ Get single product successful")
    else:
        print(f"❌ Product creation failed: {response.text}")

def test_customer_profile(customer_token):
    """Test customer profile operations"""
    print("\n=== Testing Customer Profile ===")
    
    headers = {
        'Authorization': f'Bearer {customer_token}',
        'Content-Type': 'application/json'
    }
    
    # Get customer profile
    response = requests.get(f'{BASE_URL}/customers/', headers=headers)
    print(f"Get Customer Profile: {response.status_code}")
    if response.status_code == 200:
        print("✅ Get customer profile successful")
        profile = response.json()
        print(f"Customer ID: {profile.get('id', 'Not found')}")
    else:
        print(f"❌ Get customer profile failed: {response.text}")
    
    # Update customer profile
    profile_data = {
        "phone": "+1234567890",
        "address": "456 Updated Street, New City"
    }
    
    response = requests.patch(f'{BASE_URL}/customers/', json=profile_data, headers=headers)
    print(f"Update Customer Profile: {response.status_code}")
    if response.status_code == 200:
        print("✅ Customer profile update successful")
    else:
        print(f"❌ Customer profile update failed: {response.text}")

def test_category_operations():
    """Test category operations"""
    print("\n=== Testing Category Operations ===")
    
    # Get all categories (public)
    response = requests.get(f'{BASE_URL}/categories/')
    print(f"Get All Categories: {response.status_code}")
    if response.status_code == 200:
        print("✅ Get categories successful")
        categories = response.json()
        print(f"Total categories: {len(categories)}")
        
        if categories:
            # Get products by category
            category_id = categories[0]['id']
            response = requests.get(f'{BASE_URL}/categories/{category_id}/products/')
            print(f"Get Products by Category: {response.status_code}")
            if response.status_code == 200:
                print("✅ Get products by category successful")

def run_comprehensive_tests():
    """Run all API tests"""
    print("🚀 Starting Comprehensive API Testing\n")
    
    # Get tokens
    customer_token = test_login()
    admin_token = test_admin_login()
    
    if not customer_token or not admin_token:
        print("❌ Failed to get authentication tokens. Stopping tests.")
        return
    
    # Run tests
    test_category_operations()
    test_product_operations(admin_token)
    test_customer_profile(customer_token)
    test_cart_operations(customer_token)
    test_order_operations(customer_token, admin_token)
    
    print("\n🎉 Comprehensive API testing completed!")

if __name__ == "__main__":
    run_comprehensive_tests()
