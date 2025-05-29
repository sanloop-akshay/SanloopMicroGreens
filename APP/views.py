from django.shortcuts import render,redirect
from .models import Category,Product,UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import random

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



def otp(request):
    return render(request,"auth/otp.htm")


def favorite(request):
    return render(request,"main/favorite.htm")

def cart(request):
    return render(request,"main/cart.htm")




"""
AUTHENTICATION & AUTHORIZATION
"""


def signup(request):
    if request.method == 'POST':
        # Collect form data
        request.session['signup_data'] = {
            'fullname': request.POST.get('fullname'),
            'street': request.POST.get('street'),
            'city': request.POST.get('city'),
            'district': request.POST.get('district'),
            'state': request.POST.get('state'),
            'pincode': request.POST.get('pincode'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }

        email = request.session['signup_data']['email']

        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('signup')

        otp_code = str(random.randint(100000, 999999))
        request.session['otp'] = otp_code

        send_mail(
            subject='Your OTP Code',
            message=f'Your verification OTP is: {otp_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return redirect('otp')

    return render(request, 'auth/signup.htm')


def otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        data = request.session.get('signup_data')

        if input_otp == session_otp:
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password']
            )

            UserProfile.objects.create(
                user=user,
                fullname=data['fullname'],
                street=data['street'],
                city=data['city'],
                district=data['district'],
                state=data['state'],
                pincode=data['pincode']
            )

            request.session.pop('signup_data')
            request.session.pop('otp')

            return redirect('home')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "auth/otp.htm")



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/signin.htm')



def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            messages.error(request, "No account found with this email.")
            return redirect('forgetpassword')

        otp_code = random.randint(100000, 999999)

        request.session['reset_otp'] = str(otp_code)
        request.session['reset_email'] = email

        send_mail(
            subject='Password Reset OTP',
            message=f'Your password reset OTP is: {otp_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('reset_password_otp')

    return render(request, "auth/forgetpassword.htm")

def reset_password_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if entered_otp == request.session.get('reset_otp'):
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP, try again.')

    return render(request, 'auth/resetpassotp.htm')



def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        print(new_password,confirm_password)
        if new_password != confirm_password:
            messages.error(request, "Passwords don't match.")
            return redirect('reset_password')

        email = request.session.get('reset_email')
        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgetpassword')

        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        request.session.pop('reset_otp', None)
        request.session.pop('reset_email', None)

        messages.success(request, "Password reset successfully. Please login.")
        return redirect('login')

    return render(request, 'auth/resetpassword.htm')



@require_POST
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.fullname = request.POST.get('fullname')
        profile.street = request.POST.get('street')
        profile.city = request.POST.get('city')
        profile.district = request.POST.get('district')
        profile.state = request.POST.get('state')
        profile.pincode = request.POST.get('pincode')
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')  # reload page after update

    return render(request, "main/profile.htm", {'profile': profile})