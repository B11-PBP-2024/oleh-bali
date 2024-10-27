from django import forms
from django.utils.html import strip_tags
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
        
        cleaned_data['product_name'] = strip_tags(cleaned_data.get('product_name', ''))
        cleaned_data['description'] = strip_tags(cleaned_data.get('description', ''))
        cleaned_data['product_image'] = strip_tags(cleaned_data.get('product_image', ''))
        cleaned_data['price'] = cleaned_data.get('price')  

        if not cleaned_data.get('product_name'):
            self.add_error('product_name', "Please enter a product name.")
        if not cleaned_data.get('description'):
            self.add_error('description', "Please enter a description.")
        if not cleaned_data.get('product_image'):
            self.add_error('product_image', "Please provide an image.")
        if not cleaned_data.get('product_category'):
            self.add_error('product_category', "Please select a product category.")
        if not isinstance(cleaned_data.get('price'), int):
            self.add_error('price', "Price must be a valid integer.")

        return cleaned_data


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
        cleaned_data['product'] = cleaned_data.get('product')
        cleaned_data['price'] = cleaned_data.get('price')

        if not cleaned_data.get('product'):
            self.add_error('product', "Please select a product.")
        
        if not cleaned_data.get('price'):
            self.add_error('price', "Please enter a price.")
        
        if not isinstance(cleaned_data.get('price'), int):
            self.add_error('price', "Price must be a valid integer.")

        return cleaned_data