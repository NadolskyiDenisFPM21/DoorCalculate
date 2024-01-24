from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_filtered_data/', views.get_filtered_data, name='get_filtered_data'),
    path('set_table_cookies/', views.set_table_cookies, name='set_table_cookies'),
    path('get_door_info/', views.get_door_info, name='get_door_info'),
    path('get_dimensions_aperture/', views.get_dimensions_aperture, name='get_dimensions_aperture'),
    path('get_dimensions_frame/', views.get_dimensions_frame, name='get_dimensions_frame'),
    path('get_back_width/', views.get_back_width, name='get_back_width'),
]
