import requests
import json

# Login to get token
login_data = {
    "username": "testuser",
    "password": "testpass123"
}

login_response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
print("Login response:", login_response.status_code)
print("Login content:", login_response.json())

if login_response.status_code == 200:
    token = login_response.json()['tokens']['access']
    print(f"Token: {token}")
    
    # Test cart functionality
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    cart_data = {
        "product": 1,
        "num_of_products": 2
    }
    
    print("\nTesting cart add...")
    cart_response = requests.post('http://127.0.0.1:8000/api/cart/', json=cart_data, headers=headers)
    print("Cart response status:", cart_response.status_code)
    print("Cart response content:", cart_response.text)
else:
    print("Login failed")
