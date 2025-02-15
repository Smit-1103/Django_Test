from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, Client, Order

# Register other models
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)

# Customize the Client admin panel
@admin.register(Client)
class ClientAdmin(UserAdmin):  # Inherit from Django's built-in UserAdmin
    list_display = ('username', 'email', 'company', 'city', 'province')
    fieldsets = UserAdmin.fieldsets + (  # Add extra fields to user panel
        ('Additional Info', {'fields': ('company', 'shipping_address', 'city', 'province', 'interested_in')}),
    )


