from django.shortcuts import redirect,render
from .models import Order,Payment
from Cart.models import CartItem
from .forms import OrderForm
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
    return render(request,'orders/payment.html')