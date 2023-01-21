from django.contrib import admin
from .models import Order,OrderProduct,Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['user','full_names','status','order_number','phone_number','email','country'  ,'city','order_total','tax','is_ordered','created_at','ip']
    list_filter=['is_ordered','status','country']
    list_per_page=20
    search_fields=['first_name','last_name','phone_number','email']
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)