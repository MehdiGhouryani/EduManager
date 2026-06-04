from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    # استاد
    path('instructor/course/<int:course_id>/', views.assignment_list_instructor, name='list_instructor'),
    path('instructor/course/<int:course_id>/create/', views.assignment_create, name='create'),
    path('instructor/assignment/<int:pk>/edit/', views.assignment_edit, name='edit'),
    path('instructor/assignment/<int:pk>/delete/', views.assignment_delete, name='delete'),
    path('instructor/assignment/<int:pk>/submissions/', views.submissions_for_assignment, name='submissions'),
    path('instructor/submission/<int:pk>/grade/', views.grade_submission, name='grade'),
    
    # دانشجو
    path('student/course/<int:course_id>/', views.assignment_list_student, name='list_student'),
    path('student/assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit'),
]