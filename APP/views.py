from django.shortcuts import render
from .models import Category
# Create your views here.

def home(request):
    return render(request,"main/home.htm")

def categories(request):
    categories_data = Category.objects.all()
    return render(request,"main/categories.htm",{'categories_data':categories_data})


def productCategory(request,productCategory):
    return render(request,"main/products.htm")


def product(request,productCategory,product):
    return render(request,"main/product.htm")


def contactus(request):
    return render(request,"main/contact.htm")