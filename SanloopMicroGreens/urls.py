
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
    path('login',views.login,name="login"),
    path('sign-up',views.signup,name="signup"),
    path("forget-password",views.forgetpassword,name="forgetpassword"),
    path('otp',views.otp,name="otp"),
    path('cart',views.cart,name="cart"),
    path('favorite',views.favorite,name="favorite")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)