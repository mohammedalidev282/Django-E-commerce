from django.db import models
import os
import datetime
#model user use
from django.contrib.auth.models import User

def getfilefunction(instance,filename):
    now_time=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)
#shop app 1 table category
class Category(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    image=models.ImageField(upload_to=getfilefunction,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-default 1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
#shop app 2 table product
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False,blank=False)
    vendor=models.CharField(max_length=100,null=False,blank=False)
    Pr_image=models.ImageField(upload_to=getfilefunction,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=False,blank=False)
    oldPrice=models.IntegerField(null=False,blank=False)
    newPrice=models.IntegerField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-default 1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default 1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name     
        
  #cart model
class  Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    pr_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

