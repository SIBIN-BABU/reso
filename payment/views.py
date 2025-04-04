from django.shortcuts import render,redirect
from cart.cart import Cart

from pro.models import Profile
from django.conf import settings

from pro.forms import UserInfoForm
from.models import ShippingAdddress,Order,OrderItem
from.forms import ShippingForm,CardDetails
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from pro.models import Product

#paypal stuffs 
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid #duplicate id for paypal
# Create your views here.
def payment_success(request):
    return render(request,"payment_success.html")

def payment_failed(request):
    return render(request,"payment_failed.html")


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
        
        #get the host
        
        host = request.get_host()
        #create paypal form dictionary
        paypal_dict = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' : totals,
            'item_name' : 'product_order',
            'no_shipping' : '2',
            'invoice'  : str(uuid.uuid4()),
            'currency_code' : 'EUR',
            'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return': 'https://{}{}'.format(host, reverse("payment_failed")),
            
            
        }
        
        #create actual paypal form button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        
        if request.user.is_authenticated:
            form_card =CardDetails()
            return render(request,"billing_info.html",{"paypal_form":paypal_form,"product":product,"quantities":quantities,"totals":totals,"form":request.POST,"form_card":form_card})
        else:
            form_card =CardDetails()
            return render(request,"billing_info.html",{"paypal_form":paypal_form,"product":product,"quantities":quantities,"totals":totals,"form":request.POST,"form_card":form_card})
            
        
        
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
        
    
    
def order(request, pk):
    cart = Cart(request)
    totals = cart.get_totals()  # Assuming this returns the cart total price

    if request.user.is_authenticated:
        try:
            orders = Order.objects.get(id=pk)
            orderitems = OrderItem.objects.filter(order=pk)

            # Calculate total considering sale price if available
            order_total = 0
            for item in orderitems:
                if hasattr(item.product, "sale_price") and item.product.sale_price:
                    price = item.product.sale_price  # Use sale price if available
                else:
                    price = item.product.price  # Otherwise, use regular price
                
                order_total += price * item.quantity

            return render(request, "order.html", {
                "orders": orders,
                "orderitems": orderitems,
                "totals": order_total
            })
        except Order.DoesNotExist:
            messages.error(request, "Order not found!")
            return redirect('index')
    else:
        messages.error(request, "Access denied!")
        return redirect('index')




def order_details(request):
    
    if request.user.is_authenticated:
        current_user = request.user
        order = Order.objects.filter(user = current_user)
        
    
    return render(request,"order_details.html",{"order":order})