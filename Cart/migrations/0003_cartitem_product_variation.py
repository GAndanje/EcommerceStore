# Generated by Django 3.1 on 2022-10-17 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_auto_20221017_1349'),
        ('Cart', '0002_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_variation',
            field=models.ManyToManyField(blank=True, to='Store.ProductVariation'),
        ),
    ]
