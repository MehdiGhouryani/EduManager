from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from academy.models import Course, Content
from assignments.models import Submission
from .forms import CourseForm, ContentForm

@login_required
def dashboard(request):
    if not request.user.profile.is_instructor():
        raise PermissionDenied()
    courses = request.user.taught_courses.all()
    total_students = sum(course.students.count() for course in courses)
    pending_submissions = Submission.objects.filter(
        assignment__course__in=courses,
        score__isnull=True
    ).count()
    for course in courses:
        course.pending_submissions = Submission.objects.filter(
            assignment__course=course,
            score__isnull=True
        ).count()
        course.total_assignments = course.assignments.count()
    return render(request, 'instructors/dashboard.html', {
        'courses': courses,
        'total_students': total_students,
        'pending_submissions': pending_submissions,
    })

@login_required
def create_course(request):
    if not request.user.profile.is_instructor():
        raise PermissionDenied()
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

@login_required
def course_contents(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    contents = course.contents.all()
    return render(request, 'instructors/contents_list.html', {'course': course, 'contents': contents})

@login_required
def content_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.course = course
            content.save()
            messages.success(request, 'محتوا با موفقیت اضافه شد.')
            return redirect('instructors:course_contents', course_id=course.id)
    else:
        form = ContentForm()
    return render(request, 'instructors/content_form.html', {'form': form, 'course': course})

@login_required
def content_edit(request, pk):
    content = get_object_or_404(Content, pk=pk, course__instructor=request.user)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'محتوا ویرایش شد.')
            return redirect('instructors:course_contents', course_id=content.course.id)
    else:
        form = ContentForm(instance=content)
    return render(request, 'instructors/content_form.html', {'form': form, 'course': content.course})

@login_required
def content_delete(request, pk):
    content = get_object_or_404(Content, pk=pk, course__instructor=request.user)
    course_id = content.course.id
    content.delete()
    messages.success(request, 'محتوا حذف شد.')
    return redirect('instructors:course_contents', course_id=course_id)

@login_required
def course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    students = course.students.all()
    students_data = []
    for student in students:
        submissions = Submission.objects.filter(student=student.user, assignment__course=course)
        quiz_attempts = student.quizattempt_set.filter(quiz__course=course)
        total_score = 0
        total_possible = 0
        for sub in submissions:
            if sub.score is not None:
                total_score += sub.score
                total_possible += sub.assignment.max_score
        for qa in quiz_attempts:
            total_score += qa.score * (qa.quiz.questions.count() / 100)  # convert to out of max possible
            total_possible += qa.quiz.questions.count()
        avg_percent = (total_score / total_possible * 100) if total_possible > 0 else 0
        students_data.append({
            'student': student,
            'submissions_count': submissions.count(),
            'submissions_graded': submissions.filter(score__isnull=False).count(),
            'quiz_attempts_count': quiz_attempts.count(),
            'avg_score': round(avg_percent, 1),
        })
    return render(request, 'instructors/course_students.html', {'course': course, 'students_data': students_data})