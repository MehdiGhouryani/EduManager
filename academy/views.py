from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Student, Content

def register_student(request):
    if request.method == 'POST':
        # دریافت اطلاعات از فرم
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # ایجاد کاربر جدید
        from django.contrib.auth.models import User
        user = User.objects.create_user(username=username, password=password, email=email)
        Student.objects.create(user=user, phone=phone)
        
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/register.html')

@login_required
def dashboard(request):
    try:
        student = request.user.student
        enrolled_courses = student.enrolled_courses.all()
    except:
        enrolled_courses = []
    
    context = {
        'student': getattr(request.user, 'student', None),
        'courses': enrolled_courses,
    }
    return render(request, 'academy/dashboard.html', context)

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'academy/course_list.html', {'courses': courses})

@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    is_enrolled = hasattr(request.user, 'student') and course in request.user.student.enrolled_courses.all()
    contents = course.contents.all()
    return render(request, 'academy/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'contents': contents,
    })

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user.student.enrolled_courses.filter(id=course.id).exists():
        messages.info(request, "شما قبلاً در این دوره ثبت‌نام کرده‌اید.")
    elif course.is_full():
        messages.error(request, "ظرفیت دوره تکمیل شده است.")
    else:
        request.user.student.enrolled_courses.add(course)
        messages.success(request, f"با موفقیت در دوره {course.title} ثبت‌نام شدید.")
    return redirect('course_detail', slug=slug)