from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# from .views import product

class Product(models.Model):
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    digital = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image')
    
    
    def __str__(self):
        return self.name
    
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200)
    bio = models.TextField()
    
    def __str__(self):
        return str(self.user)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.Model)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.customer} -- {self.id}'
    
    
    @property
    def get_cart_total(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.product.price * item.quantity
        return total

    @property  # Add @property decorator
    def get_cart_items(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.quantity
        return total
            
    
    
class Orderitem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
