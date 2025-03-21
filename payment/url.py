
from django.urls import path
from  .import views





urlpatterns = [
   path("",views.payment_sucess,name="payment_sucess"),
   path("chechout/",views.checkout,name="checkout"),
   path("billing_info/",views.billing_info,name="billing_info"),
   path("payment/",views.payment_info,name="payment"),
   path("shipped_item/",views.shipped_item,name="shipped_item"),
   path("unshipped_item/",views.unshipped_item,name="unshipped_item"),
   path("order/<int:pk>/",views.order,name="order")
   
   
  
]
