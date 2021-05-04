from django.contrib import admin
from .models import Buyer, Cart
# Register your models here.

admin.site.register([Buyer, Cart])
