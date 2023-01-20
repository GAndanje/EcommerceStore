# Generated by Django 3.1 on 2023-01-18 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0007_auto_20230115_1953'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Store', '0003_auto_20221017_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('Complete', 'Complete'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted')], default='New', max_length=100)),
                ('order_number', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('address_line_1', models.CharField(max_length=50)),
                ('address_line_2', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('order_total', models.FloatField()),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('tax', models.FloatField()),
                ('order_note', models.CharField(blank=True, max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cart.cartitem')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('amount_paid', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.productvariation')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]