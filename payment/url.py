
from django.urls import path,include
from  .import views





urlpatterns = [
   path("payment_success/", views.payment_success, name="payment_success"),
   path("payment_failed/",views.payment_failed,name="payment_failed"),
   path("chechout/",views.checkout,name="checkout"),
   path("billing_info/",views.billing_info,name="billing_info"),
   path("payment/",views.payment_info,name="payment"),
   path("shipped_item/",views.shipped_item,name="shipped_item"),
   path("unshipped_item/",views.unshipped_item,name="unshipped_item"),
   path("order/<int:pk>/",views.order,name="order"),
   path("paypal",include("paypal.standard.ipn.urls")),
   path("order_details/",views.order_details,name="order_details")

   
  
]
