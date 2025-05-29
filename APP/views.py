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



def contactus(request):
    return render(request,"main/contact.htm")


def login(request):
    return render(request,"auth/signin.htm")


def forgetpassword(request):
    return render(request,"auth/forgetpassword.htm")


def signup(request):
    return render(request,"auth/signup.htm")

def otp(request):
    return render(request,"auth/otp.htm")


def favorite(request):
    return render(request,"main/favorite.htm")

def cart(request):
    return render(request,"main/cart.htm")