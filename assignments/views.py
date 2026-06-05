from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from academy.models import Course
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm

# ======================== ویوهای استاد ========================

@login_required
def assignment_list_instructor(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.profile.is_instructor() or course.instructor != request.user:
        raise PermissionDenied()
    assignments = course.assignments.all()
    return render(request, 'assignments/assignment_list_instructor.html', {
        'course': course,
        'assignments': assignments,
    })

@login_required
def assignment_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.profile.is_instructor() or course.instructor != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "تکلیف با موفقیت ایجاد شد.")
            return redirect('assignments:list_instructor', course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_form.html', {'form': form, 'course': course})

@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not request.user.profile.is_instructor() or assignment.course.instructor != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "تکلیف ویرایش شد.")
            return redirect('assignments:list_instructor', course_id=assignment.course.id)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/assignment_form.html', {'form': form, 'course': assignment.course})

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not request.user.profile.is_instructor() or assignment.course.instructor != request.user:
        raise PermissionDenied()
    course_id = assignment.course.id
    assignment.delete()
    messages.success(request, "تکلیف حذف شد.")
    return redirect('assignments:list_instructor', course_id=course_id)

@login_required
def submissions_for_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not request.user.profile.is_instructor() or assignment.course.instructor != request.user:
        raise PermissionDenied()
    submissions = assignment.submissions.all()
    return render(request, 'assignments/submission_list.html', {
        'assignment': assignment,
        'submissions': submissions,
    })

@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    assignment = submission.assignment
    if not request.user.profile.is_instructor() or assignment.course.instructor != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')
        submission.score = score
        submission.feedback = feedback
        submission.save()
        messages.success(request, "نمره و بازخورد ثبت شد.")
        from notifications.models import Notification


        Notification.objects.create(
            user=submission.student,
            message=f"استاد {request.user.get_full_name()} به تکلیف '{assignment.title}' نمره {score} داد.",
            link=f"/assignments/student/course/{assignment.course.id}/"
        )
        return redirect('assignments:submissions', pk=assignment.id)
    return render(request, 'assignments/grade_form.html', {'submission': submission})

# ======================== ویوهای دانشجو ========================

@login_required
def assignment_list_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.profile.is_student():
        raise PermissionDenied()
    if not course.students.filter(user=request.user).exists():
        raise PermissionDenied()
    assignments = course.assignments.all()
    # بررسی ارسال‌های قبلی
    submissions = {sub.assignment_id: sub for sub in Submission.objects.filter(student=request.user, assignment__course=course)}
    return render(request, 'assignments/assignment_list_student.html', {
        'course': course,
        'assignments': assignments,
        'submissions': submissions,
    })

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = assignment.course
    if not request.user.profile.is_student():
        raise PermissionDenied()
    if not course.students.filter(user=request.user).exists():
        raise PermissionDenied()
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.error(request, "شما قبلاً برای این تکلیف فایل ارسال کرده‌اید.")
        return redirect('assignments:list_student', course_id=course.id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, "فایل شما با موفقیت ارسال شد.")
            return redirect('assignments:list_student', course_id=course.id)
    else:
        form = SubmissionForm()
    return render(request, 'assignments/submission_form.html', {'form': form, 'assignment': assignment})