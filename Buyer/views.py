from django.shortcuts import render, HttpResponse, redirect
from Ecom1.models import Product, Seller
from django.forms.models import model_to_dict
from .models import Cart, Order, Buyer, Ratings
from django.db import connection
# Create your views here.
import pandas as pd

def recommend(request, page):
    uuu = request.session["b_id"]
    user_index = request.session["b_id"] - 1
    recommended_products = []
    recently_reviewed = []

    if Product.objects.all().count() > 5 and Ratings.objects.filter(status__gt=4).count() > 4 and Ratings.objects.get(user_id=uuu).status > 4:
        current_user = Ratings.objects.get(user_id=uuu)
        p_a = current_user.p_a
        p_b = current_user.p_b
        p_c = current_user.p_c
        r_a = current_user.r_a
        r_b = current_user.r_b
        r_c = current_user.r_c
        my_data = [(p_a, r_a), (p_b, r_b), (p_c, r_c)]

        ratings = pd.read_csv("try1.csv", index_col=0)

        # def standarize(row):
        #     # div = row.max() - row.min()
        #     # if div == 0:
        #     #     div = 1
        #     new_row = (row - row.mean())/(row.max() - row.min())
        #     return new_row

        # ratings_std = ratings.apply(standarize)
        # ratings_std = ratings_std.fillna(0)
        item_similarity = cosine_similarity(ratings.T)
        item_similarity_df = pd.DataFrame(
            item_similarity, index=ratings.columns, columns=ratings.columns)

        def get_similar_products(product_name, user_rating):
            similar_score = item_similarity_df[product_name]*(user_rating - 2.5)
                
            similar_score = similar_score.sort_values(ascending=False)
            return similar_score

        similar_products = pd.DataFrame()
        for product, rating in my_data:
            similar_products = similar_products.append(
                get_similar_products(product, rating))
        result = similar_products.sum().sort_values(ascending=False)
        result = result.to_dict()
        counter = 0

        cur = connection.cursor()
        query = ''' SELECT "Ecom1_product".product_id,"Ecom1_product".product_name,
                    "Ecom1_product".product_image,"Ecom1_product".product_details,
                    "Ecom1_product".product_model,"Ecom1_product".product_price,
                    "Ecom1_product".product_category,"Ecom1_product".seller_id_id FROM "Ecom1_product" where "Ecom1_product".product_id=%s '''
        for i in result:
            counter = counter + 1
            cur.execute(
                '''select exists(select 1 from "Ecom1_product" where "Ecom1_product".product_id=%s)''', [i, ])
            found_flag = cur.fetchone()
            if (found_flag[0]):
                cur.execute(query, [i, ])
                recommended_product = cur.fetchone()
                recommended_products.append(recommended_product)
                if(counter == 11 and page == 'home'):
                    break
                if(counter == 31 and page == 'other'):
                    break
        # print(recommended_products)
        cur.close()
        recommended_products.pop()
        for i in range(3):
            recently_reviewed.append(recommended_products.pop(i))
        return {'error_msg': 'false', 'recommended_products': recommended_products, 'recent':recently_reviewed}
    return {'error_msg': 'true', 'recommended_products': recommended_products}


def recommended(request):
    res = recommend(request, 'home')
    return HttpResponse(res)


def bLogin(request):
    if(request.method == "POST" and request.POST["type"] == "buyer"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = Buyer.objects.get(
            buyer_name=username, buyer_password=password)
        if user:
            request.session["b_id"] = user.buyer_id
            return redirect("allProducts")
        else:
            return HttpResponse("No user found.")


def logout(request):
   del request.session["b_id"]
   return redirect("login") 

def allProducts(request):
    all_products = Product.objects.all()
    len(all_products)
    context = {"products": all_products}

    recommended_result = recommend(request, 'home')
    context["recommended_result"] = (recommended_result)
    return render(request, 'Buyer/all_products.html', context=context)


def productDetails(request, id):
    if request.method == "GET":
        product = Product.objects.get(product_id=id)
        product = model_to_dict(product)

        file_data = pd.read_csv('try1.csv')
        ratings = file_data.at[request.session["b_id"] -
                               1, str(product["product_id"])]
        context = {"product": product, "r1": range(1,
                                                   ratings+1), "r2": range(ratings+1, 6)}
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
    newItem = Cart(product_id=product_instance,
                   buyer_id=buyer_instance)
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
    query = ''' SELECT "Buyer_order".order_id, "Buyer_order".seller_id, "Buyer_order".quantity, "Buyer_order".order_placed, "Buyer_order".order_status,
    "Ecom1_product".product_id,"Ecom1_product".product_image,"Ecom1_product".product_price FROM "Buyer_order"
    INNER JOIN "Ecom1_product" ON "Ecom1_product".product_id = "Buyer_order".product_id 
    WHERE "Buyer_order".buyer_id = %s '''
    cursor.execute(query, [request.session["b_id"]])
    myOrders = cursor.fetchall()
    print(type(myOrders))
    context = {"orders": myOrders}
    return render(request, "Order/my_order.html", context)


def rateProduct(request, pid, ratings):
    uid = request.session["b_id"]
    cur = connection.cursor()

    query = ''' SELECT buyer_name FROM "Buyer_buyer" WHERE buyer_id=%s'''
    cur.execute(query, [uid, ])
    user_name = cur.fetchone()

    # thisProduct = Product.objects.get(product_id=pid)
    # pname = thisProduct.product_name
    if(Ratings.objects.filter(user_id=uid).exists()):
        rated_product = Ratings.objects.filter(user_id=uid)
        rated_product = rated_product[0]
        status = rated_product.status
        if status % 3 == 1:
            rated_product.status = status + 1
            rated_product.p_a = pid
            rated_product.r_a = ratings
            rated_product.save()
        elif status % 3 == 2:
            rated_product.status = status + 1
            rated_product.p_b = pid
            rated_product.r_b = ratings
            rated_product.save()
        elif status % 3 == 0:
            rated_product.status = status + 1
            rated_product.p_c = pid
            rated_product.r_c = ratings
            rated_product.save()
    else:
        query = ''' INSERT INTO "Buyer_ratings" (user_id,user_name,p_c,r_c,status)
                    VALUES(%s, %s, %s, %s, %s)'''
        cur.execute(query, [uid, user_name, pid, ratings, 1])

    h = str(pid)
    v = uid - 1
    file_data = pd.read_csv('try1.csv')
    file_data.at[v, h] = ratings
    # print(file_data.to_string(index=False))
    file_data.to_csv('try1.csv', index=False)

    cur.close()
    return redirect("productDetails", id=pid)


def logout(request):
    del request.session["b_id"]
    return render(request, "login.html")
