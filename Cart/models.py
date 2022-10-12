from email.policy import default
from django.db import models
from Store.models import Product
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250)
    added_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,models.CASCADE)
    cart=models.ForeignKey(Cart,models.CASCADE)
    is_active=models.BooleanField(default=True)
    quantity=models.IntegerField()

    def __str__(self):
        return self.product
    def sub_total(self):
        return self.quantity*self.product.price