
from django.contrib import admin
from django.urls import path,include
from APP import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('',views.home,name="home"),
    path('categories',views.categories,name="categories"),
    path('categories/<int:productCategory>',views.productCategory,name="productCategories"),
    path('products/<int:id>',views.specificproduct,name="specificproduct"),
    path('contactus',views.contactus,name="contactus"),
    path('login/',views.user_login,name="login"),
    path('sign-up',views.signup,name="signup"),
    path("forget-password",views.forgetpassword,name="forgetpassword"),
    path('otp',views.otp,name="otp"),
    path('cart',views.cart,name="cart"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('favorite',views.favorite,name="favorite"),
    path('reset-password-otp', views.reset_password_otp, name='reset_password_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('profile',views.profile,name="profile"),
    path('error',views.error,name="error"),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),

    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    