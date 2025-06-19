from django.shortcuts import render,redirect
from .models import Category,Product,UserProfile,Favorite
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
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random,json



def home(request):
    return render(request,"main/home.htm")

def categories(request):
    categories_data = Category.objects.all()
    return render(request,"main/categories.htm",{'categories_data':categories_data})


def productCategory(request,productCategory):
    if Product.objects.filter(category=productCategory):
        productCategoryData = Product.objects.filter(category=productCategory)
        return render(request,"main/products.htm",{'productCategoryData':productCategoryData,'productCategory':productCategory})
    else:
        return redirect("categories")



def contactus(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', 'N/A')
        inquiry_type = request.POST.get('inquiry_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')



        html_message = f"""
        <h2>New Contact Inquiry</h2>
        <table border="1" cellspacing="0" cellpadding="8" style="border-collapse: collapse; font-family: Arial, sans-serif;">
            <tr><th align="left">First Name</th><td>{first_name}</td></tr>
            <tr><th align="left">Last Name</th><td>{last_name}</td></tr>
            <tr><th align="left">Email</th><td>{email}</td></tr>
            <tr><th align="left">Phone</th><td>{phone}</td></tr>
            <tr><th align="left">Inquiry Type</th><td>{inquiry_type}</td></tr>
            <tr><th align="left">Subject</th><td>{subject}</td></tr>
            <tr><th align="left">Message</th><td>{message.replace('\n', '<br>')}</td></tr>
        </table>
        """

        send_mail(
            subject=f"Contact Form Submission: {subject}",
            message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            html_message=html_message,
        )

        return render(request, "main/contact.htm", {"success": True})

    return render(request, "main/contact.htm")







@login_required
def favorite(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        favorites = Favorite.objects.filter(user=user_profile).select_related('product')
    except UserProfile.DoesNotExist:
        favorites = []

    return render(request, "main/favorite.htm", {"favorites": favorites})


def cart(request):
    return render(request,"main/cart.htm")


def specificproduct(request, id):
    product = get_object_or_404(Product, id=id)
    
    related_products = Product.objects.filter(
        category=product.category, 
        in_stock=True
    ).exclude(id=product.id).order_by('-popular', '-id')[:4]
    
    categories = Category.objects.all()
    
    discount_percentage = 0
    if product.old_price and product.old_price > product.new_price:
        discount_percentage = round(((product.old_price - product.new_price) / product.old_price) * 100)
    
    savings_amount = 0
    if product.old_price and product.old_price > product.new_price:
        savings_amount = product.old_price - product.new_price
    
    context = {
        'product': product,
        'related_products': related_products,
        'categories': categories,
        'discount_percentage': discount_percentage,
        'savings_amount': savings_amount,
    }
    
    return render(request, "main/specificproduct.htm", context)



def specificproduct(request, id):
    product = get_object_or_404(Product, id=id)
    
    related_products = Product.objects.filter(
        category=product.category, 
        in_stock=True
    ).exclude(id=product.id).order_by('-popular', '-id')[:4]
    
    categories = Category.objects.all()
    
    discount_percentage = 0
    if product.old_price and product.old_price > product.new_price:
        discount_percentage = round(((product.old_price - product.new_price) / product.old_price) * 100)
    
    savings_amount = 0
    if product.old_price and product.old_price > product.new_price:
        savings_amount = product.old_price - product.new_price
    
    # Check if product is in user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            is_favorite = Favorite.objects.filter(user=user_profile, product=product).exists()
        except UserProfile.DoesNotExist:
            is_favorite = False
    
    context = {
        'product': product,
        'related_products': related_products,
        'categories': categories,
        'discount_percentage': discount_percentage,
        'savings_amount': savings_amount,
        'is_favorite': is_favorite,
    }
    
    return render(request, "main/specificproduct.htm", context)

@login_required
@csrf_exempt
def toggle_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID required'})
            
            product = get_object_or_404(Product, id=product_id)
            user_profile = get_object_or_404(UserProfile, user=request.user)
            
            favorite_exists = Favorite.objects.filter(user=user_profile, product=product).first()
            
            if favorite_exists:
                favorite_exists.delete()
                is_favorite = False
                message = 'Removed from favorites'
            else:
                Favorite.objects.create(user=user_profile, product=product)
                is_favorite = True
                message = 'Added to favorites'
            
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



"""
AUTHENTICATION & AUTHORIZATION
"""


def signup(request):
    if request.method == 'POST':
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
            messages.error(request, "Something Went Wrong!!!")
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
        remember_me = request.POST.get('remember_me')  
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 7) 

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/signin.htm')


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            messages.error(request, "OTP sent to your email. Please verify.")
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
        return redirect('profile')  

    return render(request, "main/profile.htm", {'profile': profile})


def error(request):
    return render(request,"error/error.htm")