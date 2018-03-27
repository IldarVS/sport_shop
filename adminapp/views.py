from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UsersListView,  self).dispatch(*args, **kwargs)


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = ('__all__')
    

class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = ('__all__')
    
#    def get_context_data(self, **kwargs):
#        context = super(UsersUpdateView, self).get_context_data(**kwargs)
#        context['title'] = 'пользователи/редактирование'
#        print(context)
#        return context

class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryListView,  self).dispatch(*args, **kwargs)

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')
    

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')
    
    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

	
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    content = {
    'title': title,
    'category': category,
    'object_list': products_list,
    }
    return render(request, 'adminapp/products.html' , content)   



#class ProductListView(ListView):
#    model = Product
#    template_name = 'adminapp/products.html'
#    
##    def get_context_data(self, pk):
##        context = super(ProductListView, self).get_context_data(pk)
###        self.object = self.get_object()
##        context['title'] = 'товары категории/просмотр'
###        context['object_list'] = Product.objects.filter(pk=self.object.pk)
###    
##    
##        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


#class ProductCreateView(CreateView):    
#    model = Product
#    template_name = 'adminapp/product_update.html'
#    success_url = reverse_lazy('admin:product_create')
#    fields = ('__all__')
#    
#    def get_context_data(self, **kwargs):
#            context = super(ProductCreateView, self).get_context_data(**kwargs)
#            context['title'] = 'товары/редактирование'
#            return context
    #    
#    def get_context_data (self, **kwargs):
#        context = super(ProductCreateView, self).get_context_data(**kwargs)
#        context['title'] = 'товары/новые'
#        print(context)
#        return context
#    def dispatch(self, *args, **kwargs):
#        return super(ProductCreateView,  self).dispatch(*args, **kwargs)
#    

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    fields = ('__all__')
    
    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'товары/редактирование'
        return context

	
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:products')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        print(category)
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            print(pk)
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        #задаем начальное значение категории в форме
        product_form = ProductEditForm(initial={'category': category})
        content = {'title': title, 'update_form': product_form, 'category': category}
        
        return render(request, 'adminapp/product_new.html', content)    
# Create your views here.
