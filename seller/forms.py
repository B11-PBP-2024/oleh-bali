from django.forms import ModelForm
from seller.models import ProductEntry

class ProductEntryForm(ModelForm):
    class Meta:
        model = ProductEntry
        fields = ["product_name", "price", "description", "product_image", "product_category"]