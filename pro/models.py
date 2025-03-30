from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modefied = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(max_length=20,blank=True)
    address1 = models.CharField(max_length=20,blank=True)
    address2 = models.CharField(max_length=20,blank=True)
    city = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20,blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    old_cart = models.CharField(max_length=1000,blank=True ,null=True)
    
    def __str__(self):
        return self.user.username
    

#create a user profile by default when they signup
def create_profile(sender, instance , created ,**kwargs):
    if created:
        user_profile =Profile(user=instance)
        user_profile.save()

#automate the profilr thing
post_save.connect(create_profile,sender=User)


class ShoeSize(models.Model):
    size = models.CharField(max_length=10, blank=True)  # Sizes like "7", "8", "9", "10"

    def __str__(self):
        return self.size

class Category(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_length=7,default=0,decimal_places=2,max_digits=7)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1,max_length=50)
    description=models.CharField(max_length=50,default='',blank=True,null=True)
    image=models.ImageField(upload_to='uploads/product/') # Sizes like "7", "8", "9", "10"
    sizes = models.ManyToManyField(ShoeSize, related_name="products",blank=True)  # Store multiple sizes
    
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=7)
    
    new_product=models.BooleanField(default=False)
    outof_stock = models.BooleanField(default=False)
    Trending_products = models.BooleanField(default=False)
    
        
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return f"Image of {self.product.name if hasattr(self.product, 'name') else self.product.id}"


class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.fist_name} {self.last_name}'


class Orders(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=20,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.product
    
    


class Contact(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


from django.db import models

class UserQuery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
