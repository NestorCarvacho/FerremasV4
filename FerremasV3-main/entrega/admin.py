from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Billinginfo)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Orderdetails)
admin.site.register(Product)
admin.site.register(Shipper)
admin.site.register(Supplier)
admin.site.register(Personalinfo)