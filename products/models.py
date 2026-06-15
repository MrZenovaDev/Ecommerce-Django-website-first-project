from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    image=models.ImageField(upload_to='images/')
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField(max_length=50)
    placed_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,default='Pending')
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)

