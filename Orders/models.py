from django.db import models
from Accounts.models import Account
from Store.models import ProductVariation,Product
# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    method=models.CharField(max_length=100)
    payment_id=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id

class Order(models.Model):
    status_choice=(
    ('New','New'),
    ('Complete','Complete'),
    ('Cancelled','Cancelled'),
    ('Accepted','Accepted'),
    )
    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(max_length=100,choices=status_choice,default='New')
    order_number=models.CharField(max_length=20)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    order_total=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    tax=models.FloatField()
    order_note=models.CharField(max_length=50,blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=100)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.first_name
    
    def full_names(self):
        return self.first_name+" "+self.last_name

class OrderProduct(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    variation=models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    color=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product_name
