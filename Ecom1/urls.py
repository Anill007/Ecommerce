from django.urls import path
from . import views
from . import myApis

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.productsList, name="plist"),
    path('add_product/', views.addProduct, name="pAdd"),
    path('update_product/<int:pk>/', views.updateProduct, name="pUpdate"),
    path('delete_product/', views.deleteProduct, name="pDelete"),
    path('orderRequests/',
         views.orderRequests, name="orderRequests"),
    path('updateRequestStatus/<int:orderId>/<int:sellerId>/<str:status>/<str:action>/',
         views.updateRequestStatus, name="updateRequestStatus"),

    # api
    path('products/', views.products),
    path('product/<int:id>/', views.product),

    # myApis
    path('api_products/', myApis.productListAPI),
    path('api_product/', myApis.updateProductAPI)

]
