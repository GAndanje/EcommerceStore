from nis import cat
from django.shortcuts import render,get_object_or_404
from .models import Product
from Category.models import Category

# Create your views here.
def store(request,category_slug=None):
    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(category=categories,is_available=True)
    else:
        products=Product.objects.all().filter(is_available=True)
    context={
        'products':products,
        'products_count':products.count()
    }
    return render(request,'store/store.html',context)