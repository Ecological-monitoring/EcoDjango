# тут може фронт звертатися
from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record_list'),  # Головна сторінка
    path('create/', views.record_create, name='record_create'),  # Додати запис
]
