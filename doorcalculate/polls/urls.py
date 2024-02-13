from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_order/', views.new_order, name ='new_order'),
    # path('orders/', views.order_list, name='orders'),
    path('get_filtered_data/', views.get_filtered_data, name='get_filtered_data'),
    path('set_table/', views.set_table, name='set_table'),
    path('get_door_info/', views.get_door_info, name='get_door_info'),
    path('get_dimensions_aperture/', views.get_dimensions_aperture, name='get_dimensions_aperture'),
    path('get_dimensions_frame/', views.get_dimensions_frame, name='get_dimensions_frame'),
    path('get_back_width/', views.get_back_width, name='get_back_width'),
    path('create_excel_specification/', views.create_excel_specification, name='create_excel_specification'),
    path('create_pdf_specification/', views.create_pdf_specification, name='create_pdf_specification'),
]
