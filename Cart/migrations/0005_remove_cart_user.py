# Generated by Django 3.1 on 2023-01-11 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0004_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]
