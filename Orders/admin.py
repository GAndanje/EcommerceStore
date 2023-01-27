from django.contrib import admin
from .models import Order,OrderProduct,Payment
# Register your models here.
class OrderProductInLine(admin.TabularInline):
    model=OrderProduct
    extra=0
    readonly_fields=[ 'user','product','payment','quantity','product_price','ordered','created_at']

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','full_names','status','order_number','phone_number','email','country'  ,'city','order_total','tax','is_ordered','created_at','ip']
    list_filter=['is_ordered','status','country']
    list_per_page=20
    inlines=[OrderProductInLine]
    search_fields=['first_name','last_name','phone_number','email','order_number']
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)

