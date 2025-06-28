from django.urls import path, include, re_path
from .views import (
    viewsAuth, viewsProducts, viewsCategories, viewsSuppliers, 
    viewsCart, viewsOrder, viewsCustomer, viewsShipper
)
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="API documentation for the Ecommerce project",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Authentication endpoints
    path('api/auth/register/', viewsAuth.UserRegistrationView.as_view(), name='user_register'),
    path('api/auth/login/', viewsAuth.login_view, name='user_login'),
    path('api/auth/profile/', viewsAuth.UserProfileView.as_view(), name='user_profile'),
    
    # Category endpoints
    path('api/categories/', viewsCategories.CategoryListView.as_view(), name='category_list'),
    path('api/categories/manage/', viewsCategories.CategoryManagementView.as_view(), name='category_create'),
    path('api/categories/<int:category_id>/', viewsCategories.CategoryDetailView.as_view(), name='category_detail'),
    path('api/categories/<int:category_id>/manage/', viewsCategories.CategoryUpdateDeleteView.as_view(), name='category_update_delete'),
    path('api/categories/<int:category_id>/products/', viewsCategories.CategoryProductsView.as_view(), name='category_products'),
    
    # Product endpoints
    path('api/products/', viewsProducts.ProductListView.as_view(), name='product_list'),
    path('api/products/manage/', viewsProducts.ProductManagementView.as_view(), name='product_create'),
    path('api/products/<int:product_id>/', viewsProducts.ProductDetailView.as_view(), name='product_detail'),
    path('api/products/<int:product_id>/manage/', viewsProducts.ProductUpdateDeleteView.as_view(), name='product_update_delete'),
    
    # Supplier endpoints
    path('api/suppliers/', viewsSuppliers.SupplierListView.as_view(), name='supplier_list'),
    path('api/suppliers/manage/', viewsSuppliers.SupplierManagementView.as_view(), name='supplier_create'),
    path('api/suppliers/<int:supplier_id>/', viewsSuppliers.SupplierDetailView.as_view(), name='supplier_detail'),
    path('api/suppliers/<int:supplier_id>/manage/', viewsSuppliers.SupplierUpdateDeleteView.as_view(), name='supplier_update_delete'),
    path('api/suppliers/<int:supplier_id>/products/', viewsSuppliers.SupplierProductsView.as_view(), name='supplier_products'),
    
    # Cart endpoints
    path('api/cart/', viewsCart.CartView.as_view(), name='cart'),
    path('api/cart/clear/', viewsCart.CartClearView.as_view(), name='cart_clear'),
    path('api/cart/<int:cart_id>/', viewsCart.CartItemView.as_view(), name='cart_item'),
    
    # Order endpoints
    path('api/orders/', viewsOrder.OrderListView.as_view(), name='order_list'),
    path('api/orders/create/', viewsOrder.OrderCreateView.as_view(), name='order_create'),
    path('api/orders/<int:order_id>/', viewsOrder.OrderDetailView.as_view(), name='order_detail'),
    path('api/orders/<int:order_id>/manage/', viewsOrder.OrderUpdateView.as_view(), name='order_update'),
    
    # Swagger documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
