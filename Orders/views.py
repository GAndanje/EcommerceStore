from django.shortcuts import redirect,render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Order,Payment,OrderProduct
from Cart.models import CartItem
from .forms import OrderForm
from Store.models import Product
import datetime
import json
# Create your views here.
def place_order(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store')
    totalPrice=0
    tax=0
    grandTotal=0
    for item in cart_items:
        totalPrice+=item.product.price*item.quantity
        tax=.02*totalPrice
        grandTotal=totalPrice+tax
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone_number=form.cleaned_data['phone_number']
            data.email=form.cleaned_data['email']
            data.country=form.cleaned_data['country']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.order_note=form.cleaned_data['order_note']
            data.ip=request.META.get('REMOTE_ADDR')
            data.tax=tax
            data.order_total=grandTotal
            data.save()
            year=int(datetime.date.today().strftime('%Y'))
            date=int(datetime.date.today().strftime('%d'))
            month=int(datetime.date.today().strftime('%m'))        
            dt=datetime.date(year,month,date)
            current_date=dt.strftime("%Y%m%d")
            print(current_date)
            order_id=current_date+str(data.id)
            data.order_number=order_id
            data.save()
            context={
                'data':data,
                'cartItems':cart_items,
            }
            return render(request,'orders/payment.html',context)
        else:
            pass
    return redirect('dashboard')

def payments(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderId'])
    payment_object=Payment(user=request.user,method=body['payment_method'],payment_id=body['transId'],amount_paid=order.order_total,status=body['status'])
    payment_object.save()
    order.payment=payment_object
    order.is_ordered=True
    order.save()
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product=OrderProduct()
        order_product.user_id=request.user.id
        order_product.product_id=item.product.id
        order_product.payment=payment_object
        order_product.order_id=order.id
        order_product.quantity=item.quantity
        order_product.product_price=item.product.price
        order_product.ordered=True
        order_product.save()
        variations=item.product_variation.all()
        order_product.variation.set(variations)
        order_product.save()
        product_object=Product.objects.get(id=item.product.id)
        product_object.stock-=item.quantity
        product_object.save()
        
    CartItem.objects.filter(user=request.user).delete()
    mail_subject='Your order has been received!'
    message=render_to_string('orders/order_received.html',{
        'user':request.user,
        'order_number':order.order_number
        })
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    # move cart_items to OrderProduct table
    # clear cart
    # reduce product quantity
    # send order received email to customer
    # send transaction details on_approve via json response and redirect the user to thank you page 
    data={
        'order_number':order.order_number,
        'payment_id':payment_object.payment_id
    }
    return JsonResponse(data)


    # user=models.ForeignKey(Account,on_delete=models.CASCADE)
    # product=models.ForeignKey(Product,on_delete=models.CASCADE)
    # payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    # order=models.ForeignKey(Order,on_delete=models.CASCADE)
    # variation=models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    # quantity=models.IntegerField()
    # product_price=models.FloatField()
    # ordered=models.BooleanField(default=False)
    # created_at=models.DateField(auto_now_add=True)
    # updated_at=models.DateField(auto_now=True)        
def order_complete(request):
    order_number=request.GET.get('order_number')
    trans_id=request.GET.get('transID')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_products=OrderProduct.objects.filter(order_id=order.id)
        payment=Payment.objects.get(payment_id=trans_id)
        sub_total=0
        for product in order_products:
            sub_total+=product.quantity*product.product_price
        context={
            'order':order,
            'order_products':order_products,
            'payment':payment,
            'sub_total':sub_total
        }
        return render(request,'orders/order_complete.html',context)
    except (order.DoesNotExist,Payment.DoesNotExist):
        return redirect('home')