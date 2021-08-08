from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *


@csrf_exempt
def productListAPI(request):  # get multiple products
    if request.method == "GET":
        request.session["id"] = 4
        user_id = request.session["id"]
        all_products = Product.objects.filter(seller_id=user_id)
        all_products_s = ProductSerializer(all_products, many=True)
        return JsonResponse(all_products_s.data, status=201, safe=False)


@csrf_exempt
def updateProductAPI(request):  # get single product and update on post
    if request.method == "GET":
        productId = request.query_params.get('productId')
        seller = request.session["id"]
        product_instance = Product.objects.filter(product_id=productId,
                                                  seller_id=seller)
        if product_instance:
            product_instance_s = ProductSerializer(product_instance, many=True)
            return JsonResponse(product_instance_s.data, status=201, safe=False)
        else:
            return JsonResponse({"error": "bad request"}, status=400, safe=False)

    elif request.method == "POST":
        productId = request.query_params.get('productId')
        seller = request.session["id"]
        product_instance = Product.objects.get(product_id=productId,
                                               seller_id=seller)
        if product_instance:
            product_instance_s = ProductSerializer(
                product_instance, data=request.data, partial=True)
            if product_instance_s.is_valid():
                product_instance_s.save()
                return JsonResponse(product_instance_s.data, status=201, safe=False)

    return JsonResponse({"error": "bad request"}, status=400, safe=False)

