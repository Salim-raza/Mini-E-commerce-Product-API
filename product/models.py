from django.conf import settings
from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = (
        ("ELECTRONICS", "electronics"),
        ("LAPTOP", "laptop"),
        ("MOBILE", "mobile"),
        ("CLOTHING", "Clothing")
    )
    product_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to='product_images/')
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.id}--{self.name}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_item(self): 
        return self.product.price * self.quantity
    
    def save(self):
        self.product.stock = self.product.stock - self.quantity
        
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=(("PENDING","Pending"), ("CONFIRMED","Confirmed"), ("DELIVERED","Delivered")),
        default= "PENDING"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_item()
        return total
    

        
   
    
    
    
    