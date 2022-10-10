from Category.models import Category

def product_categories(request):
    productCategories = Category.objects.all()
    return  dict(productCategories=productCategories)