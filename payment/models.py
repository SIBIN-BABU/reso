from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from pro.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime


class ShippingAdddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name=models.CharField(max_length=125,null=True,blank=True)
    shipping_email =models.CharField(max_length=125,null=True,blank=True)
    shipping_address1=models.CharField(max_length=125,null=True,blank=True)
    shipping_address2=models.CharField(max_length=125,null=True,blank=True)
    shipping_city =models.CharField(max_length=125,null=True,blank=True)
    shipping_state=models.CharField(max_length=125,null=True,blank=True)
    shipping_zipcode =models.CharField(max_length=125,null=True,blank=True)
    shipping_country =models.CharField(max_length=125,null=True,blank=True)
    
    #dont pluralise address
    class Meta:
        verbose_name_plural ="Shipping Address"
        
    def __str__(self):
        return f'Shipping Adddress - {str(self.id)}'
    
    
    
#create a user profile by default when they signup
def create_Shipping(sender, instance , created ,**kwargs):
    if created:
        user_Shipping =ShippingAdddress(user=instance)
        user_Shipping.save()

#automate the profilr thing
post_save.connect(create_Shipping,sender=User)
    
    
    
#create order model
class Order(models.Model):
     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
     Full_name=models.CharField(max_length=20)
     email=models.EmailField(max_length=30)
     shipping_Address=models.TextField(max_length=50)
     amount_paid = models.DecimalField(max_digits=7,decimal_places=2)
     date_order=models.DateTimeField(auto_now=True)
     shipped = models.BooleanField(default=False)
     date_shipped = models.DateTimeField(blank=True,null=True)
     

     
     def __str__(self):
         return f'Order - {str(self.id)}'
     
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
     
     



#create order item model 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7,decimal_places=2 )
    
    
    def __str__(self):
        return f'order item - {str(self.id)}'
    
    
