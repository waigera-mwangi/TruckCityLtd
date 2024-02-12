from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from moneyfield import MoneyField
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.conf import settings
from accounts.models import User
from django.db.models import F, Sum

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Pole Category'
        verbose_name_plural = 'Pole Categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.name])

    # def get_absolute_url(self):
    #     return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'pole_category', on_delete=models.CASCADE,null = True,default='Wooden_poles')
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=100)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Price' )
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField()
    created_date = models.DateField(auto_now_add=True)
    updated = models.DateField(('Updated'), auto_now=True)
    in_stock = models.BooleanField(default = True, verbose_name="In stock")

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.name])

    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Pole'
        verbose_name_plural = 'Poles'

class Order(models.Model):
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pole = models.ManyToManyField('Product', through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.order.user.username}"

    def subtotal(self):
        return self.product.price * self.quantity
