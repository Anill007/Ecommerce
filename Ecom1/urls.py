from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.productsList, name="plist"),
    path('add_product/', views.addProduct, name="pAdd"),
    path('update_product/<int:pk>/', views.updateProduct, name="pUpdate"),
    path('delete_product/', views.deleteProduct, name="pDelete"),

    # api
    path('products/', views.products),
    path('product/<int:id>/', views.product),
]
