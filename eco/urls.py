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
    path('tax-results/', views.tax_results, name='tax_results'),
    path('assess-risk/', views.assess_risk, name='assess_risk'),
    path('risk-results/', views.risk_results, name='risk_results'),
    path('damage-list/', views.damage_list, name='damage_list'),
    path('add-damage-record/', views.add_damage_record, name='add_damage_record'),
    path('damage-records/', views.damage_records, name='damage_records'),
    path('calculate-damage/', views.calculate_damage, name='calculate_damage'),
    path('damage-results/', views.damage_results, name='damage_results'),
    path('add-event/', views.add_event, name='add_event'),  # Додати подію
    path('view-results/', views.view_results, name='view_results'),

]
