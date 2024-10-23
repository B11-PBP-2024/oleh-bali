import csv
from django.core.management.base import BaseCommand
from seller.models import ProductEntry

class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_name = row['product_name']
                    description = row['description']
                    product_image = row['product_image']
                    product_category = row['product_category']

                    # Create and save ProductEntry instance
                    ProductEntry.objects.create(
                        product_name=product_name,
                        description=description,
                        product_image=product_image,
                        product_category=product_category
                    )

            self.stdout.write(self.style.SUCCESS('Successfully imported products from CSV'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
