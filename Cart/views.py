from gc import set_debug
from math import prod
import re
from django.shortcuts import HttpResponse, get_object_or_404, render,redirect

from Cart.models import CartItem,Cart
from Store.models import Product
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def cart(request,cartItems=None,totalPrice=0):
    try:
        cartObject=Cart.objects.get(cart_id=request.session.session_key)
        cartItems=CartItem.objects.all().filter(cart=cartObject,is_active=True)
        for item in cartItems:
            totalPrice+=item.product.price*item.quantity
        tax=.02*totalPrice
        grandTotal=totalPrice+tax
    except ObjectDoesNotExist:
        pass
    context={
        'cartItems':cartItems,
        'totalPrice':totalPrice,
        'tax':tax,
        'grandTotal':grandTotal
    }
    return render(request,'store/cart.html',context)
def _get_session_id(request):
    session_id=request.session.session_key
    if not session_id:
        session_id=request.session.create()
    return session_id

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id) #i think the id is the autoincrementing autoassigned unique pk
    try:
        cart=Cart.objects.get(cart_id=_get_session_id(request)) #
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_get_session_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
            )
    cart_item.save()
    return redirect('cart')

def decrement_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_get_session_id(request))
    item=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=item,cart=cart)
    if cart_item.quantity<=1:
        return redirect('remove_from_cart',product_id=product_id)
    cart_item.quantity-=1
    cart_item.save()
    return redirect('cart')
    

def remove_from_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_get_session_id(request))
    item=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=item,cart=cart)
    cart_item.delete()
    return redirect('cart')
  