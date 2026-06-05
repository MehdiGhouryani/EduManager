from django.urls import path
from . import views

app_name = 'instructors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-course/', views.create_course, name='create_course'),
    path('course/<int:course_id>/contents/', views.course_contents, name='course_contents'),
    path('course/<int:course_id>/content/create/', views.content_create, name='content_create'),
    path('content/<int:pk>/edit/', views.content_edit, name='content_edit'),
    path('content/<int:pk>/delete/', views.content_delete, name='content_delete'),
    path('course/<int:course_id>/students/', views.course_students, name='course_students'),
]