
from django.urls import path
from pro import views





urlpatterns = [
   path("",views.index,name="index"),
   path("about/",views.about,name="about"),
   path("login/",views.user_login,name="login"),
   path("logout/",views.user_logout,name="logout"),
   path("update/",views.update_user,name="update"),
   path("update_password/",views.update_password,name="update_password"),
   path("update_info/",views.update_info,name="update_info"),
   path("register/",views.Register_user,name="register"),
   path("product/<int:pk>/",views.product,name="product"),
   path("category/<str:foo>/",views.category,name="category"),
   path("search/",views.search,name="search"),
   path("info/",views.info,name="info"),
   
   

]
