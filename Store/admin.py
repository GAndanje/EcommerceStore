from django.contrib import admin
from .models import Product,ProductVariation,ReviewRating
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)

class ProductVariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','created','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','is_active')
admin.site.register(ProductVariation,ProductVariationAdmin)