from nis import cat
from threading import get_ident
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Product,ReviewRating
from .forms import RatingsForm
from Orders.models import OrderProduct
from Category.models import Category
from Cart.models import CartItem
from Cart.views import _get_session_id
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.db.models import Q


# Create your views here.
def store(request,category_slug=None):
    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(category=categories,is_available=True).order_by('id')
        paginator=Paginator(products,1)
        page_num=request.GET.get('page')
        paged_products=paginator.get_page(page_num)
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,6)
        page_num=request.GET.get('page')
        paged_products=paginator.get_page(page_num)
    context={
        'page_num':page_num,
        'page':paged_products,
        'products_count':products.count()
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug=None,product_slug=None):
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_get_session_id(request),product=product).exists()
    except Exception as e:
        return e
    try:
        bought_product=OrderProduct.objects.filter(user_id=request.user.id,product_id=product.id).exists()
    except OrderProduct.DoesNotExist:
        bought_product=None
    try:
        product_reviews=ReviewRating.objects.filter(product_id=product.id,status=True)
    except ReviewRating.DoesNotExist:
        product_reviews=None
    context={
        'product':product,
        'in_cart':in_cart,
        'has_bought_product':bought_product,
        'product_reviews':product_reviews
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            paginator=Paginator(products,8)
            page_num=request.GET.get('page')
            paged_products=paginator.get_page(page_num)
        else:
            return redirect('store')
    context={
        'page_num':page_num,
        'page':paged_products,
        'products_count':products.count(),
        'search_keyword':keyword
        }
    return render(request,'store/store.html',context)

def reviews(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            reviews_=ReviewRating.objects.get(user_id=request.user.id,product_id=product_id)
            form=RatingsForm(request.POST,instance=reviews_)
            form.save()
            messages.success(request,'Thank you. Your review has been updated successfully!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=RatingsForm(request.POST)
            if form.is_valid():
                rating=ReviewRating()
                rating.user_id=request.user.id
                rating.product_id=product_id
                rating.subject=form.cleaned_data['subject']
                rating.review=form.cleaned_data['review']
                rating.rating=form.cleaned_data['rating']
                rating.ip=request.META.get('REMOTE_ADDR')
                rating.save()
                messages.success(request,'Thank you! Your review has been received. If you have any concerns please contact our support center')
                return redirect(url)
        return redirect(url)