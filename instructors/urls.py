from django.urls import path
from . import views

app_name = 'instructors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-course/', views.create_course, name='create_course'),
]