# тут може фронт звертатися
from django.urls import path
from . import views

urlpatterns = [

    path('', views.record_list, name='record_list'),
    path('create/', views.record_create, name='record_create'),
    path('edit/<int:pk>/', views.record_edit, name='record_edit'),
    path('delete/<int:pk>/', views.record_delete, name='record_delete'),
    path('calculate-tax/', views.calculate_tax, name='calculate_tax'),
    path('add-emission/', views.add_emission_record, name='add_emission_record'),
]