from django.contrib import admin
from.models import ShippingAdddress,Order,OrderItem

# Register your models here.
admin.site.register(ShippingAdddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#creeate an orderitem inline 

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
#extend our order model 

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields =["date_order"]
    fields = ["user","Full_name","email","shipped","date_shipped"]
    inlines = [OrderItemInline]
    
    
#unregister order model

admin.site.unregister(Order)

admin.site.register(Order,OrderAdmin)
