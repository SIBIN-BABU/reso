from django.shortcuts import render,redirect
from.cart import Cart
from pro.models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal



# Create your views here.
def cart_summary(request):
    cart =Cart(request)
    product = cart.get_prods
    quantities = cart.get_quants
    totals =cart.get_totals()
 
    
   
   
    cart = request.session.get('cart', {})  # Ensure it's a dictionary

    cart_products = Product.objects.filter(id__in=cart.keys())  # Products in cart
    recommended_products = Product.objects.exclude(id__in=cart_products)[:10]  # Exclude cart items
    
        
   
    return render(request,"cart_summary.html",{"product":product,"quantities":quantities,"totals":totals,'cart': cart_products,'recommended_products': recommended_products})

def cart_add(request):
    # Get the cart instance
    cart = Cart(request) 
    
    # Check if it's a POST request with action='post'
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))
        
        
        
        
        





        # Fetch product from the database
        
        product = get_object_or_404(Product, id=product_id)
       

        # Add product to cart (✅ Pass request here)
        cart.add(product=product, quantity=product_qty, request=request)

        # Get updated cart quantity
        cart_quantity = cart.__len__()

        # Success message
       

        # Return JSON response
        return JsonResponse({'qty': cart_quantity})


def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        # Get product_id from POST data
        product_id = int(request.POST.get('product_id'))
        product_qty= str(request.POST.get('product_qty'))
        
        cart.update(product=product_id,quantity=product_qty)
        
        messages.success(request,("product quantity updated in the  cart"))
        response = JsonResponse({'qty ': product_qty})
       
        return response
        #return redirect('cart_summary')
    
    
    

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        # Get product_id from POST data
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        
        
        messages.success(request,("product sucessfully deleted from the cart"))
        response = JsonResponse({'product_id ': product_id})
       
        return response


def clear_cart(request):
    if request.POST:
        cart = Cart(request)
        cart.clear()  # Assuming your Cart class has a `clear()` method
        messages.success(request, "Your cart has been cleared.")
    return redirect('cart_summary')
        