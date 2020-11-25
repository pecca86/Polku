"""project_kirjuri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from project_kirjuri.views import SalasanatAll
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include('juttu.urls', namespace='juttu')),
    path('laites/', include('laite.urls', namespace='laites')),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('test/', views.TestPage.as_view(), name="test"),
    path('aloitus/', views.AloitusPage.as_view(), name="aloitus"),
    path('salasanat/', views.SalasanatAll.as_view(), name="kaikki_salasanat"),
    #Statistics view    
    path('statistiikka/<str:year>', views.StatisticsView.as_view(), name="statistiikka"),
    path('home/<str:year>', views.home, name='home'),
    path('population-chart/<int:year>', views.population_chart, name='population-chart'), #Here we grab the JSON data
    #Search with plain html
    path('search/', views.search_view, name='etsi'),

]
