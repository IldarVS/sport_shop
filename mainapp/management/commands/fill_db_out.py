from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product

import json, os

JSON_PATH = 'mainapp/json'

def DumpJSON (file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'a') as infile:
        return json.dump(infile)

class Command (BaseCommand):
    def handle (self, *args, **options):
        categories = ProductCategory.objects.all()
        DumpJSON(categories, 'categories')
        
        products = Product.objects.all()
        DumpJSON(products,'products')

        