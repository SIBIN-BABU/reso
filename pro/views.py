from os import name
from django.shortcuts import render,redirect,get_object_or_404
from.models import Product,Category,Profile,Contact,ProductImage
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import SignUpForm,UpdateForm,PasswordForm,UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.models import ShippingAdddress
from payment.forms import ShippingForm
#paypal stuffs 
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid #duplicate id for paypal



# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,"index.html",{'products':products})

def about(request):
    return render(request,"about.html")

def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            try:
                current_user = Profile.objects.get(user=user)
                saved_cart = current_user.old_cart
            except Profile.DoesNotExist:
                saved_cart = None

            if saved_cart:
                print("Raw saved_cart from DB:", saved_cart)  # 🔍 Debug print

                try:
                    # Ensure JSON format
                    saved_cart = saved_cart.replace("'", '"')  # ✅ Convert single to double quotes
                    convert_cart = json.loads(saved_cart)  # ✅ Safe JSON conversion
                    print("Parsed JSON Cart:", convert_cart)  # 🔍 Debug print

                except json.JSONDecodeError as e:
                    print("JSON Error:", e)  # 🔍 Debug print
                    convert_cart = {}  # ✅ Use empty cart if JSON is invalid

                # Add items to session cart
                cart = Cart(request)
                for key, value in convert_cart.items():
                    try:
                        product_id = int(key)  # ✅ Convert to integer
                        quantity = int(value)  # ✅ Convert to integer
                        cart.db_add(product=product_id, quantity=quantity)
                    except ValueError:
                        continue  

            messages.success(request, "You have been logged in.")
            return redirect('index')  
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')  

    return render(request, "login.html") 


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

@login_required
def update_user(request):
    password = None
    current_user = request.user
    
    if request.method == 'POST':
        user_form = UpdateForm(request.POST, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User has been updated")
            return redirect('index')
    else:
        user_form = UpdateForm(instance=current_user)
        
    return render(request,"update_user.html",{"user_form":user_form })
    

def Register_user(request):
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            user = authenticate(request, username=username, password=password1,password2=password2 )
            
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome!")
                return redirect('update_info')
            else:
                messages.error(request, "Authentication failed. Please check your credentials.")
                return redirect('register')
        else:
            # Debug statement to print form errors
            print("Form errors:", form.errors)
            
            # Pass form with errors to template
            return render(request, "register.html", {"form": form})
    else:
        return render(request, "register.html", {"form": form})

def product(request,pk):
    product = Product.objects.get(id=pk)
    
    # Fetch related products from the same category, excluding the current product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4] 
     
    product_images =ProductImage.objects.all()
    return render(request,"product.html",{"product":product,"product_images":product_images," category": category,"related_products":related_products})


def category(request,foo):
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,"category.html",{"products":products,"category":category})
    
    except:
         messages.error(request, "There is no such category")
         redirect('index')
         

def update_password(request):
        if request.user.is_authenticated:
            current_user = request.user
            
            if request.method == 'POST':
                form = PasswordForm(current_user, request.POST)
                
           
                if form.is_valid():
                    form.save()
                    messages.success(request, "Password updated successfully!!!")
                    
                    return redirect('login')
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
                        return redirect('update_password')
                    
            else:
                form = PasswordForm(current_user)
                return render(request,"update_password.html",{"form":form})
                
        else:
            messages.success(request, "some thing error!!!")
            return redirect('index')
                    
        
def update_info(request):
    if  request.user.is_authenticated:
        

        current_user = Profile.objects.get(user__id=request.user.id)
        
        shipping_user =ShippingAdddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        shipping_form =ShippingForm(request.POST or None,instance=shipping_user)

        
        if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your details have been updated successfully!")
                return redirect('index')
        return render(request, "update_info.html", {"form": form,"shipping_form":shipping_form})
    
    
        
    else:
        messages.success(request,"you must be logged in ")
        return redirect('index')


def search(request):
    if request.POST:
        searched = request.POST.get('searched')
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) )
        
        if not searched:
            # Add a message to the request
            messages.error(request, "That product doesn't exist")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
        
        
    else:
        return render(request, 'search.html')
    
    
    
def info(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Get email from form
        message = request.POST.get('message')  # Get message from form
        
        
        Contact.objects.create(email=email, message=message)  # Save to DB
        messages.success(request, "Your message has been updated successfully!")
        return redirect('info')  # Redirect to prevent form resubmission

      

    return render(request, "info.html")






