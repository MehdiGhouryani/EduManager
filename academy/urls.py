from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'academy'

urlpatterns = [
    path('', RedirectView.as_view(url='/courses/', permanent=False), name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),  # استفاده از ویو سفارشی
    path('register/', views.register_student, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    
    # پشتیبانی کامل از حروف فارسی و اعداد در slug
    re_path(r'^courses/(?P<slug>[-\w]+)/$', views.course_detail, name='course_detail'),
    re_path(r'^courses/(?P<slug>[-\w]+)/enroll/$', views.enroll_course, name='enroll_course'),
    
    path('contents/<int:pk>/view/', views.view_content, name='view_content'),
]