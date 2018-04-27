from django.shortcuts import render
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.shortcuts import get_object_or_404
import random
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]
    data_begin = datetime.date(day=12,month=11,year=2011)
    content = { 'title': title, 'products': products, 'data_begin': data_begin}
    return render(request, 'mainapp/index.html', content)

#def jeverly(request):
#    title = 'Украшения'
##    products = Product.objects.all()[:4]
##    data_begin = datetime.date(day=12,month=11,year=2011)
##    content = {'title': title}
#    return render(request, 'mainapp/jeverly/index.php', {'title': title})


#def products(request, pk):
#    title='Товары'
#    category = get_object_or_404(ProductCategory, pk=pk)
#    products_list = Product.objects.filter(category__pk=pk).order_by('name')
#        
#    content = {
#        'title': title,
#        'category': category,
#        'objects': products_list,
#    }
    
#    return render(request, 'adminapp/products.html', content)
#def products(request, pk=None):
#    print(pk)
#    title='Товары'
#    links_menu = ProductCategory.objects.all()
#    basket = getBasket(request.user)
#    if request.user.is_authenticated:
#        basket = Basket.objects.filter(user=request.user)
#    if pk:
#        if pk == '0':
#            category = {'name': 'все'}
#            products = Product.objects.all().order_by('price')
#        else:
#            category = get_object_or_404(ProductCategory, pk=pk)
#            products = Product.objects.filter(category__pk=pk).order_by('price')
#        content = {
#            'pk': pk,
#            'title': title,
#            'links_menu': links_menu,
#            'category': category,
#            'products': products,
#            'basket': basket,
#            }
#        return render(request, 'mainapp/products_list.html', content)
#       
def products (request, pk=None, page=1):
    title = 'продукты'
#    links_menu = ProductCategory.objects.filter(is_active = True)
    links_menu = ProductCategory.objects.all()
    basket = getBasket(request.user)
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    print(pk)
    if pk:
#        if pk == '0':
#            category = {'pk': 0, 'name': 'все'}
#            products = Product.objects.filter(is_active= True, category__is_active = True).order_by('price')
#                
#        else:
#            category = get_object_or_404(ProductCategory, pk=pk)
#            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active= True).order_by('price')
        if pk == '0':
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 6)
        try :
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products' : products_paginator,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html' , content)

    
    hot_product = getHotProduct()
    same_products = getSameProducts(hot_product)
    content = {
        'pk': pk,
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products
        }
    return render(request, 'mainapp/products.html', content)

def contact(request):
    title='Контакты'
    return render(request, 'mainapp/contacts.html', 
                      {'title': title} 
                         )

def getBasket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else :
        return[]

def getHotProduct():
    products = Product.objects.all()
    return random.sample(list(products),1)[0]

def getSameProducts(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': getBasket(request.user),
    }
    
    return render(request, 'mainapp/product.html', content)
# Create your views here.

