import os
import time
from django.db import models
from django.contrib.auth.models import User


def get_timestamped_filename(filename, folder):
    ext = filename.split('.')[-1]
    new_filename = f"{int(time.time())}.{ext}"
    return os.path.join(folder, new_filename)

def timestamped_image_upload_path(instance, filename):
    return get_timestamped_filename(filename, 'category_images/')

def product_timestamped_image_upload_path(instance, filename):
    return get_timestamped_filename(filename, 'product_images/')

class Category(models.Model):
    image = models.ImageField(upload_to=timestamped_image_upload_path)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=product_timestamped_image_upload_path)
    description = models.TextField(blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


"""
AUTHENTICATION & AUTHORIZATION DATABASE
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username
    
    
class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.user.username} - {self.product.name}"
    
    
class CartItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.user.username} - {self.product.name} x{self.quantity}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Order Placed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')

    def __str__(self):
        return f"Order #{self.id} by {self.user.user.username} "


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order #{self.order.id}"