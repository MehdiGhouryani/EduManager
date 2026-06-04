from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Course, Student, Content
from .forms import StudentRegistrationForm

def custom_logout(request):
    """خروج از حساب کاربری با متد GET (برای راحتی)"""
    logout(request)
    return redirect('/')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. خوش آمدید!")
            return redirect('academy:dashboard')
        else:
            messages.error(request, "لطفاً خطاها را اصلاح کنید.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"خوش آمدید {username}.")
                return redirect('academy:dashboard')
        messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard(request):
    try:
        student = request.user.student
        enrolled_courses = student.enrolled_courses.all()
    except Student.DoesNotExist:
        student = None
        enrolled_courses = []
    return render(request, 'academy/dashboard.html', {
        'student': student,
        'courses': enrolled_courses,
    })

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'academy/course_list.html', {'courses': courses})

@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    is_enrolled = False
    if hasattr(request.user, 'student'):
        is_enrolled = course in request.user.student.enrolled_courses.all()
    contents = course.contents.all()
    return render(request, 'academy/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'contents': contents,
    })

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not hasattr(request.user, 'student'):
        messages.error(request, "ابتدا باید دانشجو باشید.")
        return redirect('academy:course_detail', slug=slug)
    student = request.user.student
    if student.enrolled_courses.filter(id=course.id).exists():
        messages.info(request, "شما قبلاً در این دوره ثبت‌نام کرده‌اید.")
    elif course.is_full():
        messages.error(request, "ظرفیت دوره تکمیل شده است.")
    else:
        student.enrolled_courses.add(course)
        messages.success(request, f"شما در دوره {course.title} ثبت‌نام شدید.")
    return redirect('academy:course_detail', slug=slug)

@login_required
def view_content(request, pk):
    content = get_object_or_404(Content, pk=pk)
    if not hasattr(request.user, 'student') or content.course not in request.user.student.enrolled_courses.all():
        messages.error(request, "شما دسترسی به این محتوا ندارید.")
        return redirect('academy:course_detail', slug=content.course.slug)
    return render(request, 'academy/view_content.html', {'content': content})