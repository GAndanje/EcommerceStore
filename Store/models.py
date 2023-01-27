from django.db import models
from django.db.models import Avg,Count
from Category.models import Category
from django.urls import reverse
from Accounts.models import Account
# Create your models here.
class Product(models.Model):
    product_name    =models.CharField(max_length=200,unique=True)
    slug            =models.SlugField(max_length=200,unique=True)
    description     =models.TextField(max_length=500,blank=True)
    price           =models.IntegerField()
    image           =models.ImageField(upload_to='photos/products') 
    stock           =models.IntegerField()
    is_available    =models.BooleanField(default=True)
    category        =models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    =models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    def average_rating(self):
        average=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        if average['average'] is not None:
            return float(average['average'])
        return 'There is no sufficient reviews to rate this product'
    def review_count(self):
        review_count=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        counter=0
        if review_count['count'] is not None:
            return review_count['count']
        return counter

# customising returned queryset
class VariationsManager(models.Manager):
    def colors(self):
        return super(VariationsManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationsManager,self).filter(variation_category='size',is_active=True)

variation_category_choices=(
    ('color','color'),
    ('size','size'),
    )
class ProductVariation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choices)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now=True)
    objects=VariationsManager()
    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    ip=models.CharField(max_length=20,blank=True)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.subject