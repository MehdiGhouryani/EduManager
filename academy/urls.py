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
    
        # مسیرهای آزمون (استاد)
    path('instructor/course/<int:course_id>/quizzes/', views.quiz_list_instructor, name='quiz_list_instructor'),
    path('instructor/course/<int:course_id>/quiz/create/', views.quiz_create, name='quiz_create'),
    path('instructor/quiz/<int:pk>/edit/', views.quiz_edit, name='quiz_edit'),
    path('instructor/quiz/<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('instructor/quiz/<int:quiz_id>/questions/', views.quiz_questions, name='quiz_questions'),
    path('instructor/quiz/<int:quiz_id>/question/create/', views.question_create, name='question_create'),
    path('instructor/question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('instructor/question/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('instructor/quiz/<int:quiz_id>/results/', views.quiz_results_instructor, name='quiz_results_instructor'),

    # مسیرهای آزمون (دانشجو)
    path('student/course/<int:course_id>/quizzes/', views.quiz_list_student, name='quiz_list_student'),
    path('student/quiz/<int:quiz_id>/take/', views.quiz_take, name='quiz_take'),
    path('student/quiz/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('student/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    # پشتیبانی کامل از حروف فارسی و اعداد در slug
    re_path(r'^courses/(?P<slug>[-\w]+)/$', views.course_detail, name='course_detail'),
    re_path(r'^courses/(?P<slug>[-\w]+)/enroll/$', views.enroll_course, name='enroll_course'),


    path('contents/<int:pk>/inline/', views.serve_pdf_inline, name='serve_pdf_inline'),
    
    path('contents/<int:pk>/view/', views.view_content, name='view_content'),
]