from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import forms
from . import models
from . import serializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Buyer.models import Order,Buyer
from django.db import connection
import shutil,os
from cloudinary.forms import cl_init_js_callbacks 

# ml modules
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

# ml codes


def resetCSV(request):
    dict = {"UserProduct": []}
    df = pd.DataFrame(dict)
    df.to_csv('try1.csv', index=False)

    # addNewProduct("iphone")
    # addNewProduct("samsung")
    # addNewProduct("nokia")

    # addNewUser("anil")
    # addNewUser("rick")
    # addNewUser("larry")
    # addNewUser("dave")

    # changeIndexValue(0, "nokia", 5)
    # changeIndexValue(0, "samsung", 1)
    # changeIndexValue(1, "samsung", 5)
    # changeIndexValue(3, "iphone", 5)

    return HttpResponse("csv cleared.")


def addNewProduct(request,new_index):
    file_data = pd.read_csv('try1.csv')
    new_column = [0] * (file_data.shape[0])
    file_data[new_index] = new_column
    file_data.to_csv('try1.csv', index=False)


def addNewUser(name):
    file_data = pd.read_csv('try1.csv')
    file_data.loc[file_data.shape[0]] = [name]+([0]*(file_data.shape[1]-1))
    file_data.to_csv('try1.csv', index=False)


def changeIndexValue(v, h, value):
    file_data = pd.read_csv('try1.csv')
    file_data.at[v, h] = value
    print(file_data.to_string(index=False))
    file_data.to_csv('try1.csv', index=False)

# Other backend logic
# Create your views here.


def home(request):
    return render(request, "login.html")


def sLogin(request):
    if(request.method == "POST" and request.POST["type"] == "seller"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = models.Seller.objects.get(
            seller_name=username, seller_password=password)
        if user:
            request.session["id"] = user.seller_id
            return redirect("plist")
        else:
            return HttpResponse("No user found.")

# 1.for getting all lists of products


def productsList(request):
    user_id = request.session['id']
    all_products = models.Product.objects.filter(seller_id=user_id)
    context = {"list": all_products, "sid": request.session['id']}
    if all_products:
        return render(request, 'products_list.html', context)
    else:
        return HttpResponse("<h1><a href='../../Ecom1/add_product'>Add a new product.</a></h1><h1>No Products Added.</h1>")


def addProduct(request):
    if request.method == "POST":
        # request params
        # print(request.POST['product_name'])
        # myfile = request.FILES['product_image']
        # print(myfile.name)
        # ---------------
        print(request.POST['seller_id'])
        print(request.session['id'])

        if (request.POST['seller_id'] != f"{request.session['id']}"):
            return HttpResponse("seller unauthorised.")
        # print form values
        # print(pForm['product_name'].value())
        # print(pForm.data['product_details'])
        # print(pForm['product_image'].value())
        # ----------------
        pForm = forms.ProductForm(request.POST, request.FILES)
        if pForm.is_valid():
            new_item_index=pForm.save()
            addNewProduct(request,str(new_item_index))
        # product_instance = models.Product(0,product_name, product_image, product_details, product_price, product_model, product_category, 3)
        # product_instance.save()

        return redirect("plist")  # change url in browser + content

    pForm = forms.ProductForm()
    context = {'form': pForm, "sid": request.session['id']}
    return render(request, 'add_product.html', context)


def updateProduct(request, pk):
    product = models.Product.objects.get(
        product_id=pk, seller_id=request.session['id'])
    pForm = forms.ProductForm(instance=product)
    if request.method == "POST":

        if (request.POST['seller_id'] != f"{request.session['id']}"):
            return HttpResponse("seller unauthorised.")

        pForm = forms.ProductForm(
            request.POST, request.FILES, instance=product)
        if pForm.is_valid():
            pForm.save()
            return redirect("plist")

    context = {'form': pForm, 'id': pk}
    return render(request, "update_product.html", context)


def deleteProduct(request):
    if request.method == "POST":
        del_index = request.POST['record']
        models.Product.objects.get(
            product_id=del_index, seller_id=request.session['id']).delete()
    return redirect("plist")


def orderRequests(request):
    cursor = connection.cursor()
    query = ''' SELECT "Buyer_order".order_id, "Buyer_order".buyer_id, "Buyer_order".seller_id, "Buyer_order".quantity, "Buyer_order".order_placed, "Buyer_order".order_status, 
    "Ecom1_product".product_id, "Ecom1_product".product_name, "Ecom1_product".product_image, "Ecom1_product".product_price FROM "Buyer_order"
            INNER JOIN "Ecom1_product" ON "Ecom1_product".product_id = "Buyer_order".product_id
            WHERE "Ecom1_product".seller_id_id = %s ORDER BY "Buyer_order".order_id'''
    cursor.execute(query, [request.session['id'], ])
    order_requests = cursor.fetchall()
    cursor.close()
    context = {"orders": order_requests}
    return render(request, "orderRequests.html", context)


def updateRequestStatus(request, orderId, sellerId, status, action):
    if sellerId == request.session["id"]:
        status_choices = ("CANCELLED", "PENDING", "APPROVED", "DELIVERED")
        next_status = "DELIVERED"
        previous_status = "CANCELLED"
        qstatus = " "

        cursor = connection.cursor()
        if action == "next":
            for i in range(3):
                if status == status_choices[i]:
                    next_status = status_choices[i+1]
            qstatus = next_status

        elif action == "previous":
            for i in range(1, 4):
                if status == status_choices[i]:
                    previous_status = status_choices[i-1]
            qstatus = previous_status

        else:
            return redirect("orderRequests")
        query = ''' UPDATE "Buyer_order" SET order_status = %s 
                WHERE order_id=%s AND seller_id=%s '''
        cursor.execute(query, [qstatus, orderId, sellerId])
        cursor.close()

    return redirect("orderRequests")
    # 1.api


@csrf_exempt
@api_view(['GET', 'POST'])
def products(request):
    if request.method == "GET":
        all_products = models.Product.objects.all()
        all_products = serializer.ProductSerializer(all_products, many=True)
        return JsonResponse(all_products.data, safe=False)

    elif request.method == "POST":
        serializedData = serializer.ProductSerializer(data=request.data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(serializedData.data, status=201)
        return JsonResponse(serializedData.errors, status=400)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def product(request, id):
    if request.method == "PUT":
        product = models.Product.objects.get(product_id=id)
        serializedData = serializer.ProductSerializer(
            product, data=request.data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(serializedData.data, status=201)
        return JsonResponse(serializedData.errors, status=400)

    elif request.method == "DELETE":
        product = models.Product.objects.get(product_id=id)
        product.delete()
        return HttpResponse("success")


def resetAll(request):

    cursor = connection.cursor()
    cursor.execute('''TRUNCATE TABLE "Buyer_cart" RESTART IDENTITY CASCADE''')
    cursor.execute('''TRUNCATE TABLE "Buyer_buyer" RESTART IDENTITY CASCADE''')
    cursor.execute('''TRUNCATE TABLE "Buyer_order" RESTART IDENTITY CASCADE''')
    cursor.execute(
        '''TRUNCATE TABLE "Ecom1_product" RESTART IDENTITY CASCADE''')
    cursor.execute(
        '''TRUNCATE TABLE "Ecom1_seller" RESTART IDENTITY CASCADE''')
    cursor.execute(
        '''TRUNCATE TABLE "Buyer_ratings" RESTART IDENTITY CASCADE''')
    cursor.close()
    return HttpResponse("success")

def resetMedia(request):
    shutil.rmtree('media')   
    os.makedirs('media')

    return HttpResponse("success")



def signUp(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        password1 = request.POST["repassword"]
        type = request.POST["type"]

        if(password == password1):
            cursor = connection.cursor()

            if type == "buyer":
                cursor.execute(
                    ''' SELECT exists(select * from "Buyer_buyer" where buyer_name = %s) ''', [username, ])
                res = cursor.fetchone()
                if res[0]:
                    return HttpResponse("user already exists.")
                else:
                    cursor.execute(''' INSERT INTO "Buyer_buyer"(buyer_name, buyer_password) values (%s,%s)''', [
                        username, password])
                    new_buyer = Buyer.objects.get(buyer_name = username)
                    cursor.execute(''' INSERT INTO "Buyer_ratings" (user_id,user_name,status)
                    VALUES(%s, %s, %s)''',[new_buyer.buyer_id,new_buyer.buyer_name,0])
                    cursor.close()
                    addNewUser(username)
                    return HttpResponse("Successfully Created")

            elif type == "seller":
                cursor.execute(
                    ''' SELECT exists(select * from "Ecom1_seller" where seller_name = %s) ''', [username, ])
                res = cursor.fetchone()
                if res[0]:
                    return HttpResponse("user already exists.")
                else:
                    cursor.execute(''' INSERT INTO "Ecom1_seller"(seller_name, seller_password) values (%s,%s)''', [
                        username, password])
                    cursor.close()
                    return HttpResponse("Successfully Created")
        else:
            return HttpResponse("retype password.")
