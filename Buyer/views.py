from django.shortcuts import render, HttpResponse, redirect
from Ecom1.models import Product, Seller
from django.forms.models import model_to_dict
from .models import Cart, Order, Buyer
from django.db import connection
# Create your views here.


def bLogin(request):
    request.session["b_id"] = 3
    return HttpResponse("buyer logged in")


def allProducts(request):
    all_products = Product.objects.all()
    context = {"products": all_products}
    return render(request, 'Buyer/all_products.html', context=context)


def productDetails(request, id):
    if request.method == "GET":
        product = Product.objects.get(product_id=id)
        product = model_to_dict(product)
        context = {"product": product}
        return render(request, 'Buyer/product.html', context=context)


def myCart(request):
    if request.method == "GET":
        cursor = connection.cursor()
        query = '''select "Buyer_cart".cart_id, "Buyer_cart".product_id_id, "Ecom1_product".product_name, "Ecom1_product".seller_id_id, "Buyer_cart".product_quantity
                    from (("Buyer_buyer" 
	                INNER JOIN "Buyer_cart" ON "Buyer_buyer".buyer_id = "Buyer_cart".buyer_id_id)
	                INNER JOIN "Ecom1_product" ON "Ecom1_product".product_id = "Buyer_cart".product_id_id
                    )WHERE "Buyer_cart".buyer_id_id = %s ORDER BY "Buyer_cart".cart_id'''
        cursor.execute(query, [request.session["b_id"], ])
        cart_items = cursor.fetchall()
        cursor.close()
        print(cart_items)
        context = {"cart_items": cart_items}
        return render(request, 'Buyer/my_cart.html', context)


def addToCart(request, id):
    buyer_instance = Buyer.objects.get(buyer_id=request.session["b_id"])
    product_instance = Product.objects.get(product_id=id)
    newItem = Cart(product_id=product_instance, buyer_id=buyer_instance)
    newItem.save()
    return redirect("allProducts")


def updateQuantity(request, id, add, sub):
    if request.method == "GET" and request.session["b_id"]:
        product_instance = Cart.objects.get(
            cart_id=id, buyer_id=request.session["b_id"])
        if product_instance.product_quantity == 1:
            sub = 0
        product_instance.product_quantity = product_instance.product_quantity + add - sub
        product_instance.save()

    return redirect("myCart")


def deleteCartItem(request, id):
    if request.session["b_id"]:
        cart_item = Cart.objects.get(
            cart_id=id, buyer_id=request.session["b_id"])
        cart_item.delete()
    return redirect("myCart")


def confirmOrder(request, id, seller_id, cart_id, quantity):
    if request.session["b_id"]:
        product_instance = Product.objects.get(
            product_id=id, seller_id=seller_id)
        seller_instance = Seller.objects.get(seller_id=seller_id)
        buyer_instance = Buyer.objects.get(buyer_id=request.session["b_id"])
        Order(product=product_instance,
              seller=seller_instance, buyer=buyer_instance, quantity=quantity).save()
        Cart.objects.get(
            cart_id=cart_id, buyer_id=request.session["b_id"]).delete()
    return redirect("myCart")


def myOrder(request):
    cursor = connection.cursor()
    query = ''' SELECT * FROM "Buyer_order"
    INNER JOIN "Ecom1_product" ON "Ecom1_product".product_id = "Buyer_order".product_id 
    WHERE "Buyer_order".buyer_id = %s '''
    cursor.execute(query, [request.session["b_id"]])
    myOrders = cursor.fetchall()
    context = {"orders": myOrders}
    return render(request, "Order/my_order.html", context)
