from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_filtered_data/', views.get_filtered_data, name='get_filtered_data'),
    path('set_table_cookies/', views.set_table_cookies, name='set_table_cookies'),
    path('get_price/', views.get_price, name='get_price'),
]
