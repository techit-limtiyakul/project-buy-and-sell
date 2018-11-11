"""UCSDBuyAndSell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

# For image serving
from django.conf import settings
from django.views.static import serve

from django.contrib.auth import views
from django.urls import path
from UCSDMarket import views as UCSDMarket
from UCSDMarket.forms import LoginForm

urlpatterns = [
	url(r'^$', UCSDMarket.Home, name="Home"),
	url(r'^market/listing/$', UCSDMarket.ListingPage, name="Listing"),
	url(r'^market/my_listings/$', UCSDMarket.MyListings, name="MyListings"),
    url(r'^market/create_listings/$', UCSDMarket.CreateListings, name="CreateListings"),
    url(r'^market/search_listings/$', UCSDMarket.SearchListings, name="SearchListings"),
    url(r'^market/import_listings/$', UCSDMarket.ImportListings, name="ImportListings"),
    url(r'^market/login/$', views.login,{'authentication_form':LoginForm}, name="Login"),
    url(r'^market/signup/$', UCSDMarket.Signup, name="Signup"),
    url(r'^market/signoff/$', UCSDMarket.Signoff, name="Signoff"),
	path('admin/', admin.site.urls),
]

#This storage method will need to be changed on python anywhere
if settings.DEBUG:
	urlpatterns += [
		url(r'^media/(?P<path>.*)$', serve, {
			'document_root': settings.MEDIA_ROOT,
		}),
		]
