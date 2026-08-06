from django.contrib import admin
from .models import Product, Category , Cart, CartItem, Order, OrderItem
class orderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone_number', 'address', 'total_price', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['user__username', 'full_name', 'phone_number', 'address']
    inlines = [orderItemInline]
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)