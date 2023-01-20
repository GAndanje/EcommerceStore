from django.db import models
from Store.models import ProductVariation
from Store.models import Product
from Accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250)
    added_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product_variation=models.ManyToManyField(ProductVariation,blank=True)
    cart=models.ForeignKey(Cart,models.CASCADE)
    is_active=models.BooleanField(default=True)
    quantity=models.IntegerField()

    def __unicode__(self):
        return self.product
    def sub_total(self):
        return self.quantity*self.product.price