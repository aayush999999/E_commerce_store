from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class ItemInsert(models.Model): 
    item_group = models.CharField(max_length=30)
    item_desc = models.CharField(max_length=30)
    stock_qty = models.IntegerField(default="")
    item_rate = models.IntegerField(default="")
    # item_date = models.DateField()
    image = models.ImageField(upload_to="seller/images", default="")

    def __str__(self):
        return self.item_desc
    



class Order(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    date_ordered = models.DateTimeField(
        auto_now_add=True
    )
    complete = models.BooleanField(
        default=False
    )
    transaction_id =models.CharField(
        max_length=100,
        null=True
    )

    def __str__(self):
        return str(self.user)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    item = models.ForeignKey(
        ItemInsert,
        on_delete=models.SET_NULL,
        null=True
        )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )
    date_added = models.DateTimeField(
       auto_now_add=True
    )

    def __str__(self):
        return str(self.order.id)

    @property
    def get_total(self):
        total = self.item.item_rate * self.quantity
        return total
    
    


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    mobile = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name    
      

class Checkout(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    orderr = models.ForeignKey(
        Order, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    final_order = models.CharField(max_length=1000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    addr = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    number = models.CharField(max_length=15, default="")
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name 
    