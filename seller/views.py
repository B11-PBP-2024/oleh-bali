from django.shortcuts import render, redirect
from .models import ProductEntry, ProductDataSet
from .forms import ProductEntryForm, CSVUploadForm
import csv

# View untuk menampilkan daftar produk
def show_products(request):
    products = ProductEntry.objects.all()  # Mengambil semua produk dari ProductEntry
    return render(request, 'products.html', {'products': products})

# View untuk menambahkan produk
def add_product(request):
    if request.method == 'POST':
        form = ProductEntryForm(request.POST)
        if form.is_valid():
            product_entry = form.save(commit=False)

            if form.cleaned_data['use_existing']:
                # Menggunakan data dari dataset yang dipilih
                product_entry.product_name = product_entry.product_dataset.product_name
                product_entry.description = product_entry.product_dataset.description
                product_entry.product_image = product_entry.product_dataset.product_image
                product_entry.product_category = product_entry.product_dataset.product_category

            product_entry.save()
            return redirect('seller:show_products')  # Mengarahkan ke daftar produk dengan namespace yang benar

    else:
        form = ProductEntryForm()

    return render(request, 'create_product.html', {'form': form})

# View untuk mengimpor data CSV
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Lewati header CSV

            for row in reader:
                product_name, price, description, product_image, product_category = row
                if not ProductDataSet.objects.filter(product_name=product_name).exists():
                    ProductDataSet.objects.create(
                        product_name=product_name,
                        price=price,
                        description=description,
                        product_image=product_image,
                        product_category=product_category
                    )

            return redirect('seller:show_products')  # Mengarahkan ke daftar produk dengan namespace yang benar
    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})
