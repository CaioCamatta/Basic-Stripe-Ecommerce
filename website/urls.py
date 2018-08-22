"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop import views
from django.conf import settings
from django.conf.urls.static import static

# Use include() here and app_name on the app.urls so you can refer to the url as app_name:url_name. Also works on a template if you use {% url 'app_name:url_name' %}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('shop/', include('shop.urls'), name='shop'),
    path('search/', include('search.urls'), name='search'),
    path('cart/', include('cart.urls'), name='cart'),
    path('order/', include('order.urls'), name='order'),
    path('account/create/', views.signUpView, name='signup'),
    path('account/login/', views.signInView, name='signin'),
    path('account/logout/', views.signOutView, name='signout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
