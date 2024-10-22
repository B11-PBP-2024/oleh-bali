from django import forms
from django.contrib.auth import get_user_model
from .models import BuyerProfile, SellerProfile

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['profile_picture', 'store_name', 'nationality']
        widgets = {
                'store_name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
                'nationality': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
            }

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['profile_picture', 'city', 'store_name', 'subdistrict', 'village', 'address','maps', 'price']
        widgets = {
                'store_name': forms.TextInput(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'price': forms.TextInput(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'city': forms.TextInput(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'subdistrict': forms.Select(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'village': forms.Select(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'address': forms.TextInput(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
                'maps': forms.URLInput(attrs={'class': 'border bg-white border-gray-300 p-2 rounded-md'}),
            }

    def __init__(self, *args, **kwargs):
        super(SellerProfileForm, self).__init__(*args, **kwargs)
        self.fields['subdistrict'].widget = forms.Select()
        self.fields['village'].widget = forms.Select()


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'price', 'description', 'category', 'photo_url', 'stock']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#             'price': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#             'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#             'category': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#             'photo_url': forms.URLInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#             'stock': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 rounded-md'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         self.fields['category'].widget = forms.Select()