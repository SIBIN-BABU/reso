from pro.models import Product
from decimal import Decimal
from pro.models import Profile

from django.contrib import messages
class Cart:
    def __init__(self, request):
        """Initialize the cart using session data."""
        self.session = request.session
        #get request
        self.request = request
        
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}  # Initialize empty cart
        self.cart = cart
        
    
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        #logic
        
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]= str( product_qty)
            
    
        self.session.modified = True
        
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            curremt_user =Profile.objects.filter(user__id=self.request.user.id)
            #convert to str {'2':1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            
            curremt_user.update(old_cart=str(carty))
        
        
    
      

    def add(self, product, quantity, request):
        product_id = int(product.id)
        product_qty = str(quantity)
        

        if product_id in self.cart:
                    messages.warning(request, "Product already added to the cart")  # 🔔 Display warning message
        else:
                    self.cart[product_id] = str(product_qty)
                
                    
                    
                    messages.success(request, "Product added to cart successfully")  # ✅ Success message

        self.session.modified = True

        
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            curremt_user =Profile.objects.filter(user__id=self.request.user.id)
            #convert to str {'2':1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            
            curremt_user.update(old_cart=str(carty))
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
    
    # Return the queryset of products
        return products
        
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        #get cart
        ourcart = self.cart
        
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
         #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            curremt_user =Profile.objects.filter(user__id=self.request.user.id)
            #convert to str {'2':1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            
            curremt_user.update(old_cart=str(carty))
        
        things = self.cart
        return things
    
    def delete(self,product):
        product_id = str(product)
        
        #delete from dictinory /cart
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            curremt_user =Profile.objects.filter(user__id=self.request.user.id)
            #convert to str {'2':1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            
            curremt_user.update(old_cart=str(carty))
        
            
           
        


    def get_totals(self):
        product_ids = [key for key in self.cart.keys() if key.isdigit()]  # ✅ Only numeric keys
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key in product_ids:
            value = self.cart[key]  # ✅ Get stored quantity (string or dictionary)

            if isinstance(value, dict):  
                quantity = int(value.get("quantity", 0))  # ✅ Extract quantity safely
            else:
                quantity = int(value)  # ✅ If it's a string, convert to int directly

            for product in products:
                if product.id == int(key):  
                    if product.is_sale:
                        total += product.sale_price * quantity
                    else:
                        total += product.price * quantity

        return total

                        


    def clear(self):
            """Clear all items from the cart"""
            self.session['cart'] = {}
            self.session.modified = True