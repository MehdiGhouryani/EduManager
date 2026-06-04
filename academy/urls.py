from django.urls import path, re_path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'academy'

urlpatterns = [
    path('', RedirectView.as_view(url='/courses/', permanent=False), name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_student, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    
    # استفاده از re_path برای پشتیبانی از حروف فارسی در slug
    re_path(r'^courses/(?P<slug>[-\w]+)/$', views.course_detail, name='course_detail'),
    re_path(r'^courses/(?P<slug>[-\w]+)/enroll/$', views.enroll_course, name='enroll_course'),
    
    path('contents/<int:pk>/view/', views.view_content, name='view_content'),
]