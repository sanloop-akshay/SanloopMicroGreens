import os
import time
from django.db import models

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