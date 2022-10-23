from django.shortcuts import HttpResponse, get_object_or_404, render,redirect

from Cart.models import CartItem,Cart
from Store.models import ProductVariation
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
    variationList=[]
    if request.method=='POST':
        for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                variation=ProductVariation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                variationList.append(variation)
            except Exception:
                pass
    try:
        cart=Cart.objects.get(cart_id=_get_session_id(request)) #
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_get_session_id(request))
        cart.save()
    cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
    if cart_item_exists:
        cart_items=CartItem.objects.filter(product=product,cart=cart)
        existing_variations=[]
        for cart_item in cart_items:
            instance_variations=cart_item.product_variation.all()
            existing_variations.append(list(instance_variations))
        if variationList in existing_variations:
            cart_item_idx=existing_variations.index(variationList)
            cart_item=cart_items[cart_item_idx]
            cart_item.quantity+=1
        else:
            cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
            cart_item.product_variation.clear()
            cart_item.product_variation.add(*variationList)
    else:
        cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
        cart_item.product_variation.clear()
        if len(variationList):
            cart_item.product_variation.add(*variationList)
    cart_item.save()
    return redirect('cart')

def decrement_cart(request,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_get_session_id(request))
    item=get_object_or_404(Product,id=product_id)
    try:
        cart_item=CartItem.objects.get(product=item,cart=cart,id=cart_item_id)
        if cart_item.quantity<=1:
            return redirect('remove_from_cart',product_id,cart_item_id)
        cart_item.quantity-=1
        cart_item.save()
    except:
        pass
    return redirect('cart')
    

def remove_from_cart(request,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_get_session_id(request))
    item=get_object_or_404(Product,id=product_id)
    try:
        cart_item=CartItem.objects.get(product=item,cart=cart,id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')
  