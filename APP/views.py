from django.shortcuts import render,redirect
from .models import Category,Product
# Create your views here.

def home(request):
    return render(request,"main/home.htm")

def categories(request):
    categories_data = Category.objects.all()
    return render(request,"main/categories.htm",{'categories_data':categories_data})


def productCategory(request,productCategory):
    if Product.objects.filter(category=productCategory):
        productCategoryData = Product.objects.filter(category=productCategory)
        return render(request,"main/products.htm",{'productCategoryData':productCategoryData})
    else:
        return redirect("categories")


def product(request,productCategory,product):
    return render(request,"main/product.htm")


def contactus(request):
    return render(request,"main/contact.htm")