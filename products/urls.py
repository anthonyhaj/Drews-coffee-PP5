from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.all_products, name='products'),
]
