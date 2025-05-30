
from django.contrib import admin
from django.urls import path
from APP import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('categories',views.categories,name="categories"),
    path('categories/<int:productCategory>',views.productCategory,name="productCategories"),
    path('contactus',views.contactus,name="contactus"),
    path('login',views.user_login,name="login"),
    path('sign-up',views.signup,name="signup"),
    path("forget-password",views.forgetpassword,name="forgetpassword"),
    path('otp',views.otp,name="otp"),
    path('cart',views.cart,name="cart"),
    path('favorite',views.favorite,name="favorite"),
    path('reset-password-otp', views.reset_password_otp, name='reset_password_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('profile',views.profile,name="profile"),
    path('error',views.error,name="error"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    