from django import forms
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
            "product_name", "product_image", "product_details", "product_price", "product_model", "product_category", "seller_id"]
