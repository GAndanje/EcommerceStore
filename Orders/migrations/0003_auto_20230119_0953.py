# Generated by Django 3.1 on 2023-01-19 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_remove_order_cart_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
