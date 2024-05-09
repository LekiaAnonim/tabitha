from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ShopView.as_view(), name='home'),
    path('shop/<str:slug>', views.CategoryProductView.as_view(), name='category'),
    path('check-out', views.CheckOut.as_view() , name='checkout'),
    path('user-account', views.UserAccountView.as_view() , name='account'),
]