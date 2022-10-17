from django.contrib import admin
from .models import Cart,CartItem
# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')
admin.site.register(CartItem,CartItemAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','added_date')
admin.site.register(Cart,CartAdmin)