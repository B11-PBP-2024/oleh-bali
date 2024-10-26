from django import forms 
from .models import ProductEntry, ProductSeller

class ProductEntryForm(forms.ModelForm):
    price = forms.IntegerField(required=True, label='Price')

    class Meta:
        model = ProductEntry
        fields = ['product_name', 'description', 'product_image', 'product_category']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].required = False
        self.fields['description'].required = False
        self.fields['product_image'].required = False
        self.fields['product_category'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('product_name'):
            self.add_error('product_name', "Please enter a product name.")
        if not cleaned_data.get('description'):
            self.add_error('description', "Please enter a description.")
        if not cleaned_data.get('product_image'):
            self.add_error('product_image', "Please provide an image.")
        if not cleaned_data.get('product_category'):
            self.add_error('product_category', "Please select a product category.")


class ProductSellerForm(forms.ModelForm):
    class Meta:
        model = ProductSeller
        fields = ['product', 'price']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['product'].queryset = ProductEntry.objects.all()
        self.fields['product'].widget.attrs['readonly'] = True  
        self.fields['price'].required = True  

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('product'):
            self.add_error('product', "Please enter a product name.")
        if not cleaned_data.get('price'):
            self.add_error('price', "Please enter a price.")
