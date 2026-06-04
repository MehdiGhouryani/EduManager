from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from academy.models import Course
from .forms import CourseForm  

@login_required
def dashboard(request):
    if not request.user.profile.is_instructor():
        raise PermissionDenied
    courses = request.user.taught_courses.all()
    total_students = sum(course.students.count() for course in courses)
    return render(request, 'instructors/dashboard.html', {
        'courses': courses,
        'total_students': total_students,
    })

@login_required
def create_course(request):
    if not request.user.profile.is_instructor():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "دوره با موفقیت ایجاد شد.")
            return redirect('instructors:dashboard')
    else:
        form = CourseForm()
    
    return render(request, 'instructors/course_form.html', {'form': form})