from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Vendor
from django.utils.text import slugify
from apps.product.models import Product
from .forms import ProductForm

# Create your views here.
def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request,user)

            vendor=Vendor.objects.create(name=user.username,created_by=user)

            return redirect('frontpage')
        
    else:
        form=UserCreationForm()  

    return render(request,'vendors/become_vendor.html',{'form':form})

@login_required
def vendor_admin(request):
    vendor=request.user.vendor
    products=vendor.products.all()
    return render(request,'vendors/vendor_admin.html',{'vendor':vendor,'products':products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.vendor=request.user.vendor
            product.slug=slugify(product.title)
            product.save()
            return redirect('vendor_admin')
    else:
        form=ProductForm()
    
    return render(request,'vendors/add_product.html',{'form':form})
