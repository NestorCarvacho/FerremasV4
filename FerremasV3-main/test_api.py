#!/usr/bin/env python3
"""
Simple API testing script for the Django ecommerce API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_auth():
    """Test authentication endpoints"""
    print("=== Testing Authentication ===")
    
    # Test login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if response.status_code == 200:
        print("✓ Login successful")
        data = response.json()
        token = data.get('access_token') or data.get('access')
        if token:
            print(f"  Token: {token[:20]}...")
            return token
        else:
            print("  No token received")
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"  Response: {response.text}")
    
    return None

def test_categories(token=None):
    """Test categories endpoints"""
    print("\n=== Testing Categories ===")
    
    # Test GET categories (should work without auth)
    response = requests.get(f"{BASE_URL}/api/categories/")
    if response.status_code == 200:
        print("✓ GET categories successful")
        categories = response.json()
        print(f"  Found {len(categories)} categories")
    else:
        print(f"✗ GET categories failed: {response.status_code}")
    
    # Test POST category (requires auth)
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        category_data = {
            "category_name": "Test Category",
            "description": "A test category created via API"
        }
        
        response = requests.post(f"{BASE_URL}/api/categories/", json=category_data, headers=headers)
        if response.status_code == 201:
            print("✓ POST category successful")
            category = response.json()
            print(f"  Created category ID: {category.get('category_id')}")
            return category.get('category_id')
        else:
            print(f"✗ POST category failed: {response.status_code}")
            print(f"  Response: {response.text}")
    
    return None

def test_products(token=None, category_id=None):
    """Test products endpoints"""
    print("\n=== Testing Products ===")
    
    # Test GET products (should work without auth)
    response = requests.get(f"{BASE_URL}/api/products/")
    if response.status_code == 200:
        print("✓ GET products successful")
        products = response.json()
        print(f"  Found {len(products)} products")
    else:
        print(f"✗ GET products failed: {response.status_code}")
    
    # Test products by category if we have a category
    if category_id:
        response = requests.get(f"{BASE_URL}/api/categories/{category_id}/products/")
        if response.status_code == 200:
            print(f"✓ GET products by category {category_id} successful")
            products = response.json()
            print(f"  Found {len(products)} products in category")
        else:
            print(f"✗ GET products by category failed: {response.status_code}")

def test_user_registration():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    
    user_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "user_type": "customer",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=user_data)
    if response.status_code == 201:
        print("✓ User registration successful")
        user = response.json()
        print(f"  Created user: {user.get('username')}")
    else:
        print(f"✗ User registration failed: {response.status_code}")
        print(f"  Response: {response.text}")

def main():
    """Run all tests"""
    print("Testing Django Ecommerce API")
    print("=" * 40)
    
    # Test authentication
    token = test_auth()
    
    # Test categories
    category_id = test_categories(token)
    
    # Test products
    test_products(token, category_id)
    
    # Test user registration
    test_user_registration()
    
    print("\n=== API Testing Complete ===")

if __name__ == "__main__":
    main()
