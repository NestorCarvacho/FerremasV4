# Django Ecommerce API - Complete Setup

## 🎉 Setup Status: COMPLETE ✅

Your Django ecommerce API is fully configured and ready for development!

## 📋 What's Included

- ✅ **Django REST Framework** - Complete API framework
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **CORS Headers** - Cross-origin resource sharing
- ✅ **SQLite Database** - Development database with sample data
- ✅ **Custom User Model** - Extended user management
- ✅ **Comprehensive API** - All ecommerce endpoints
- ✅ **Swagger Documentation** - Interactive API docs
- ✅ **Test Suite** - Comprehensive API testing

## 🚀 Quick Start

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Access API Documentation
- **Swagger UI**: http://127.0.0.1:8000/
- **ReDoc**: http://127.0.0.1:8000/redoc/

### 3. Test Credentials
- **Admin**: `admin` / `admin123`
- **Customer**: `testuser` / `testpass123`

### 4. Run Tests
```bash
python comprehensive_test.py
```

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | User registration | None |
| POST | `/api/auth/login/` | User login | None |
| GET | `/api/auth/profile/` | User profile | Token |

### Categories
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/categories/` | List categories | None |
| POST | `/api/categories/manage/` | Create category | Admin |
| GET | `/api/categories/{id}/` | Category detail | None |
| PUT/PATCH | `/api/categories/{id}/manage/` | Update category | Admin |
| DELETE | `/api/categories/{id}/manage/` | Delete category | Admin |
| GET | `/api/categories/{id}/products/` | Category products | None |

### Products
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/products/` | List products | None |
| POST | `/api/products/manage/` | Create product | Admin |
| GET | `/api/products/{id}/` | Product detail | None |
| PUT/PATCH | `/api/products/{id}/manage/` | Update product | Admin |
| DELETE | `/api/products/{id}/manage/` | Delete product | Admin |

### Suppliers
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/suppliers/` | List suppliers | Token |
| POST | `/api/suppliers/manage/` | Create supplier | Admin |
| GET | `/api/suppliers/{id}/` | Supplier detail | Token |
| PUT/PATCH | `/api/suppliers/{id}/manage/` | Update supplier | Admin |
| DELETE | `/api/suppliers/{id}/manage/` | Delete supplier | Admin |
| GET | `/api/suppliers/{id}/products/` | Supplier products | Token |

### Cart (Customer Only)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/cart/` | Get cart items | Customer |
| POST | `/api/cart/` | Add to cart | Customer |
| PUT | `/api/cart/{id}/` | Update cart item | Customer |
| DELETE | `/api/cart/{id}/` | Remove cart item | Customer |
| DELETE | `/api/cart/clear/` | Clear cart | Customer |

### Orders (Customer Only)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/orders/` | List orders | Customer |
| POST | `/api/orders/create/` | Create order | Customer |
| GET | `/api/orders/{id}/` | Order detail | Customer |
| PUT/PATCH | `/api/orders/{id}/manage/` | Update order | Admin |

## 🔐 Authentication

### Login Request
```json
POST /api/auth/login/
{
    "username": "testuser",
    "password": "testpass123"
}
```

### Response
```json
{
    "message": "Login successful",
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {
        "id": 2,
        "username": "testuser",
        "email": "test@test.com",
        "user_type": "customer"
    }
}
```

### Using Tokens
Include the access token in the Authorization header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📝 Sample API Calls

### 1. Create Category (Admin)
```bash
curl -X POST http://127.0.0.1:8000/api/categories/manage/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category_name": "Electronics",
    "description": "Electronic devices"
  }'
```

### 2. Add Product to Cart (Customer)
```bash
curl -X POST http://127.0.0.1:8000/api/cart/ \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "num_of_products": 2
  }'
```

### 3. Create Order (Customer)
```bash
curl -X POST http://127.0.0.1:8000/api/orders/create/ \
  -H "Authorization: Bearer YOUR_CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main St",
    "shipping_city": "City",
    "shipping_postal_code": "12345",
    "shipping_country": "Country"
  }'
```

## 🛠️ Management Commands

### Create Sample Data
```bash
python manage.py create_sample_data
```

### Create Admin User
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Testing

### Run All Tests
```bash
python comprehensive_test.py
```

### Test Individual Components
```bash
# Test authentication only
python -c "from comprehensive_test import EcommerceAPITester; t=EcommerceAPITester(); t.test_authentication()"

# Test cart functionality
python test_cart.py
```

## 📁 Project Structure

```
FerremasV3-main/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                  # SQLite database
├── comprehensive_test.py       # Complete API test suite
├── setup_complete.py          # Setup summary script
├── apiIntegracion/            # Django project settings
│   ├── settings.py           # Main configuration
│   └── urls.py               # Main URL routing
└── entrega/                   # Main Django app
    ├── models.py             # Database models
    ├── serializers.py        # API serializers
    ├── urls.py               # App URL patterns
    ├── views/                # API views
    │   ├── viewsAuth.py     # Authentication views
    │   ├── viewsCart.py     # Cart management
    │   ├── viewsCategories.py # Category management
    │   ├── viewsProducts.py  # Product management
    │   ├── viewsSuppliers.py # Supplier management
    │   └── viewsOrder.py     # Order management
    └── management/commands/   # Custom management commands
```

## 🔄 Next Development Steps

1. **Frontend Integration**
   - Create React/Vue.js frontend
   - Implement responsive design
   - Add customer dashboard

2. **Enhanced Features**
   - Product image uploads
   - Search and filtering
   - Product reviews/ratings
   - Inventory management

3. **Payment Integration**
   - Stripe/PayPal integration
   - Multiple payment methods
   - Order confirmation emails

4. **Performance & Security**
   - Add caching (Redis)
   - Implement rate limiting
   - Add comprehensive logging
   - Security auditing

5. **Deployment**
   - Containerize with Docker
   - Deploy to AWS/Heroku
   - Set up CI/CD pipeline
   - Configure production database

## 🆘 Troubleshooting

### Server Won't Start
```bash
# Check for migration issues
python manage.py makemigrations
python manage.py migrate

# Check for port conflicts
netstat -an | findstr :8000
```

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py create_sample_data
```

### Authentication Errors
- Ensure JWT tokens haven't expired (15 minutes default)
- Check user permissions (admin vs customer)
- Verify token format in Authorization header

## 📚 Documentation Links

- **Django REST Framework**: https://www.django-rest-framework.org/
- **Django JWT**: https://django-rest-framework-simplejwt.readthedocs.io/
- **Django CORS**: https://github.com/adamchainz/django-cors-headers
- **drf-yasg (Swagger)**: https://drf-yasg.readthedocs.io/

---

🎯 **Your Django Ecommerce API is ready for development!**

Access the interactive documentation at: http://127.0.0.1:8000/
