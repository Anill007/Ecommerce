from django.urls import path
from . import views

urlpatterns = [
    path('login', views.bLogin, name="bLogin"),
    path('logout', views.logout, name="logout"),
    path('allProducts/', views.allProducts, name="allProducts"),
    path('myCart/', views.myCart, name="myCart"),
    path('product/<int:id>/', views.productDetails, name="productDetails"),
    path('addToCart/<int:id>/', views.addToCart, name="addToCart"),
    path('updateQuantity/<int:id>/<int:add>/<int:sub>/',
         views.updateQuantity, name="updateQuantity"),
    path('deleteCartItem/<int:id>/', views.deleteCartItem, name="deleteCartItem"),
    path('confirmOrder/<int:id>/<int:seller_id>/<int:cart_id>/<int:quantity>',
         views.confirmOrder, name="confirmOrder"),
    path('myOrder/', views.myOrder, name="myOrder"),
    path('rateProduct/<int:pid>/<int:ratings>',
         views.rateProduct, name="rateProduct"),
     path('recommended/', views.recommended, name="recommended"),
     path('logout/', views.logout, name="logout"),
]
