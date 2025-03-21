from django.shortcuts import render,redirect
from cart.cart import Cart
from pro.models import Profile
from pro.forms import UserInfoForm
from.models import ShippingAdddress,Order,OrderItem
from.forms import ShippingForm,CardDetails
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from pro.models import Product
# Create your views here.
def payment_sucess(request):
    return render(request,"payment_success.html")



def checkout(request):
    cart =Cart(request)
    product = cart.get_prods
    quantities = cart.get_quants
    totals =cart.get_totals
    
    if  request.user.is_authenticated:
        current_user = ShippingAdddress.objects.get(user__id=request.user.id)
        
       
        form = ShippingForm(request.POST or None, instance=current_user)
        return render(request,"checkout.html",{"product":product,"quantities":quantities,"totals":totals,"form":form})
        
    else:
        form = ShippingForm(request.POST or None)
        
        return render(request,"checkout.html",{"product":product,"quantities":quantities,"totals":totals,"form":form})
        
    
def billing_info(request):
    
    if request.POST:
    
      
        cart =Cart(request)
        product = cart.get_prods
        quantities = cart.get_quants
        totals =cart.get_totals
        
        #create a session with user info
        my_shipping=request.POST
        request.session['my_shipping'] = my_shipping
        
        if request.user.is_authenticated:
            form_card =CardDetails()
            return render(request,"billing_info.html",{"product":product,"quantities":quantities,"totals":totals,"form":request.POST,"form_card":form_card})
        else:
            form_card =CardDetails()
            return render(request,"billing_info.html",{"product":product,"quantities":quantities,"totals":totals,"form":request.POST,"form_card":form_card})
            
        
        
    else:
        return redirect('index')
    
def payment_info(request):
    if request.POST:
        
        
        cart =Cart(request)
        product = cart.get_prods
        quantities = cart.get_quants
        totals =cart.get_totals()
        
        
        card_detail = CardDetails(request.POST or None)
        
        my_shipping = request.session.get('my_shipping')
        
        
        #gather order info
        full_name =my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #create shipping Address for session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n {my_shipping['shipping_country']}"
        amount_paid = totals
        
        
        #create an order
        if request.user.is_authenticated:
            user = request.user
            
            #create order
            create_order=Order(user=user,Full_name=full_name,email=email,shipping_Address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            #Add order item
            
            #get orderid
            order_id=create_order.pk
            
            #get product info
            for product in product():
                
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                    
                else:
                    price = product.price
                    
                #get quantity
                
                for key,value in quantities().items():
                    if int(key) == product.id:
                        
                        #create order item 
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
                       
                        create_order_item.save()
                        
                        
            for key in list(request.session.keys()):
                if key == "cart":
                    del request.session[key]          
            
            #delete the cart from db
            
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")
            
            
            
            
            
            
            messages.success(request,"order saved !!")
        else:
            
            create_order=Order(Full_name=full_name,email=email,shipping_Address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            #get orderid
            order_id=create_order.pk
            
            #get product info
            for product in product():
                
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                    
                else:
                    price = product.price
                    
                #get quantity
                
                for key,value in quantities().items():
                    if int(key) == product.id:
                        
                        #create order item 
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
                        
                        create_order_item.save()
                        
            for key in list(request.session.keys()):
                if key == "cart":
                    del request.session[key] 
            
            
            
        
        return redirect('index')
        
      
        
    else:
        return redirect('index')
    
    
    

def shipped_item(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        
        
        order = Order.objects.filter(shipped=True)
        return render(request,"shipped_item.html",{"order":order }) 
    else:
        messages.success(request,"Access denied  !!")
        return redirect('index')
            



def unshipped_item(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.filter(shipped=False)
        return render(request,"unshipped_item.html",{"order":order}) 
    else:
        messages.success(request,"Access denied  !!")
        return redirect('index')
        
    
    
def order(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.get(id=pk)
        orderitem  = OrderItem.objects.filter(order=pk)
        print(orderitem)
        return render(request,"order.html",{"orders":orders,"orderitem":orderitem}) 
    else:
        messages.success(request,"Access denied  !!")
        return redirect('index')
        