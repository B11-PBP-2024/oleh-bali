from django import forms
from .models import ProductEntry, ProductDataSet

class ProductEntryForm(forms.ModelForm):
    use_existing = forms.BooleanField(required=False, label="Use existing product from dataset")

    class Meta:
        model = ProductEntry
        fields = ['use_existing', 'product_dataset', 'product_name', 'price', 'description', 'product_image', 'product_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengisi pilihan product_dataset dengan data dari ProductDataSet
        self.fields['product_dataset'].queryset = ProductDataSet.objects.all()
        self.fields['product_dataset'].required = False
        self.fields['product_name'].required = False
        self.fields['description'].required = False
        self.fields['product_image'].required = False
        self.fields['product_category'].required = False

    def clean(self):
        cleaned_data = super().clean()
        use_existing = cleaned_data.get('use_existing')

        if use_existing:
            if not cleaned_data.get('product_dataset'):
                self.add_error('product_dataset', "Please select a product from the dataset.")
        else:
            if not cleaned_data.get('product_name'):
                self.add_error('product_name', "Please enter a product name.")
            if not cleaned_data.get('description'):
                self.add_error('description', "Please enter a description.")
            if not cleaned_data.get('product_image'):
                self.add_error('product_image', "Please provide an image.")
            if not cleaned_data.get('product_category'):
                self.add_error('product_category', "Please select a product category.")

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")
