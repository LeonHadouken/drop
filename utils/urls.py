from django.urls import path
from . import views

urlpatterns = [
    path('types/', views.view_types, name='view_types'),
]
