from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Course, Student, Content
from .forms import StudentRegistrationForm
from django.utils import timezone
from django.db import transaction
from .models import Quiz, Question, QuizAttempt
from .forms import QuizForm, QuestionForm
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count
from assignments.models import Submission   # اضافه شود
from .forms import LoginForm   # اضافه شود
from django_ratelimit.decorators import ratelimit


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
            return redirect('academy:dashboard')   # اصلاح شد
        else:
            messages.error(request, "لطفاً خطاها را اصلاح کنید.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@ratelimit(key='ip', rate='8/h', method='POST')
def login_view(request):
    
    if getattr(request, 'limited', False):
        messages.error(request, "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً یک ساعت بعد تلاش کنید.")
        return render(request, 'registration/login.html', {'form': form})


    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600)  # ۲ هفته
            else:
                request.session.set_expiry(0)        # تا بسته شدن مرورگر
            messages.success(request, f"خوش آمدید {user.username}.")
            return redirect('academy:dashboard')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})




@login_required
def dashboard(request):
    try:
        student = request.user.student
        enrolled_courses = student.enrolled_courses.all()
        
        # محاسبه آمار تکالیف
        submissions = Submission.objects.filter(student=request.user)
        submitted_count = submissions.count()
        avg_score = submissions.filter(score__isnull=False).aggregate(Avg('score'))['score__avg']
        if avg_score:
            avg_score = round(avg_score, 1)
        else:
            avg_score = '-'
            
    except Student.DoesNotExist:
        student = None
        enrolled_courses = []
        submitted_count = 0
        avg_score = '-'
    
    return render(request, 'academy/dashboard.html', {
        'student': student,
        'courses': enrolled_courses,
        'submitted_count': submitted_count,
        'avg_score': avg_score,
    })

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'academy/course_list.html', {'courses': courses})


@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    is_enrolled = False
    assignments = course.assignments.all()
    quizzes = course.quizzes.all()
    
    submitted_ids = []
    quiz_attempted_ids = []
    submitted_count = 0
    attempted_quizzes = 0
    avg_score = None
    scores_list = []
    
    if hasattr(request.user, 'student'):
        student = request.user.student
        is_enrolled = course in student.enrolled_courses.all()
        if is_enrolled:
            # دریافت شناسه تکالیف ارسال شده
            submitted_ids = Submission.objects.filter(student=request.user, assignment__course=course).values_list('assignment_id', flat=True)
            submitted_count = submitted_ids.count()
            # دریافت نمرات تکالیف نمره‌خورده
            graded_subs = Submission.objects.filter(student=request.user, assignment__course=course, score__isnull=False)
            scores_list = [sub.score for sub in graded_subs]
            if scores_list:
                avg_score = sum(scores_list) / len(scores_list)
            # دریافت شناسه آزمون‌های انجام شده
            quiz_attempted_ids = QuizAttempt.objects.filter(student=student, quiz__course=course).values_list('quiz_id', flat=True)
            attempted_quizzes = quiz_attempted_ids.count()
    
    contents = course.contents.all()
    
    return render(request, 'academy/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'contents': contents,
        'assignments': assignments,
        'quizzes': quizzes,
        'submitted_ids': list(submitted_ids),
        'quiz_attempted_ids': list(quiz_attempted_ids),
        'submitted_count': submitted_count,
        'attempted_quizzes': attempted_quizzes,
        'avg_score': avg_score,
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




# ======================== ویوهای استاد برای مدیریت آزمون ========================

@login_required
def quiz_list_instructor(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    quizzes = course.quizzes.all()
    return render(request, 'academy/quiz_list_instructor.html', {'course': course, 'quizzes': quizzes})

@login_required
def quiz_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, 'آزمون با موفقیت ایجاد شد.')
            return redirect('academy:quiz_list_instructor', course_id=course.id)
    else:
        form = QuizForm()
    return render(request, 'academy/quiz_form.html', {'form': form, 'course': course})

@login_required
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, course__instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'آزمون ویرایش شد.')
            return redirect('academy:quiz_list_instructor', course_id=quiz.course.id)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'academy/quiz_form.html', {'form': form, 'course': quiz.course})

@login_required
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, course__instructor=request.user)
    course_id = quiz.course.id
    quiz.delete()
    messages.success(request, 'آزمون حذف شد.')
    return redirect('academy:quiz_list_instructor', course_id=course_id)

# مدیریت سوالات

@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, course__instructor=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'سوال با موفقیت اضافه شد.')
            return redirect('academy:quiz_questions', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'academy/question_form.html', {'form': form, 'quiz': quiz})

@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk, quiz__course__instructor=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'سوال ویرایش شد.')
            return redirect('academy:quiz_questions', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'academy/question_form.html', {'form': form, 'quiz': question.quiz})

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, quiz__course__instructor=request.user)
    quiz_id = question.quiz.id
    question.delete()
    messages.success(request, 'سوال حذف شد.')
    return redirect('academy:quiz_questions', quiz_id=quiz_id)

@login_required
def quiz_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, course__instructor=request.user)
    questions = quiz.questions.all()
    return render(request, 'academy/quiz_questions.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_results_instructor(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, course__instructor=request.user)
    attempts = quiz.quizattempt_set.all().select_related('student__user')
    return render(request, 'academy/quiz_results_instructor.html', {'quiz': quiz, 'attempts': attempts})

# ======================== ویوهای دانشجو برای شرکت در آزمون ========================

@login_required
def quiz_list_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.students.filter(user=request.user).exists():
        raise PermissionDenied()
    quizzes = course.quizzes.all()
    # پیدا کردن آزمون‌هایی که دانشجو قبلاً انجام داده است
    attempted_ids = QuizAttempt.objects.filter(student__user=request.user, quiz__course=course).values_list('quiz_id', flat=True)
    return render(request, 'academy/quiz_list_student.html', {
        'course': course,
        'quizzes': quizzes,
        'attempted_ids': attempted_ids,
    })

@login_required
def quiz_take(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    course = quiz.course
    # بررسی عضویت دانشجو در دوره
    if not course.students.filter(user=request.user).exists():
        raise PermissionDenied()
    # بررسی اینکه قبلاً شرکت نکرده باشد
    if QuizAttempt.objects.filter(quiz=quiz, student__user=request.user).exists():
        messages.error(request, 'شما قبلاً در این آزمون شرکت کرده‌اید.')
        return redirect('academy:quiz_list_student', course_id=course.id)
    
    # ذخیره سوالات در session برای استفاده در طی آزمون (یا می‌توان مستقیماً در قالب نمایش داد)
    questions = list(quiz.questions.all())
    request.session['quiz_questions'] = [q.id for q in questions]
    request.session['quiz_id'] = quiz.id
    request.session['quiz_start_time'] = timezone.now().isoformat()
    
    return render(request, 'academy/quiz_take.html', {
        'quiz': quiz,
        'questions': questions,
        'question_count': len(questions),
    })

@login_required
def quiz_submit(request, quiz_id):
    if request.method != 'POST':
        return redirect('academy:quiz_list_student', course_id=quiz.course.id)
    
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    course = quiz.course
    if not course.students.filter(user=request.user).exists():
        raise PermissionDenied()
    if QuizAttempt.objects.filter(quiz=quiz, student__user=request.user).exists():
        messages.error(request, 'تقلب ممنوع! شما قبلاً امتحان داده‌اید.')
        return redirect('academy:quiz_list_student', course_id=course.id)
    
    # دریافت پاسخ‌های ارسالی
    answers = {}
    for key, value in request.POST.items():
        if key.startswith('q_'):
            q_id = int(key.split('_')[1])
            answers[q_id] = int(value) if value.isdigit() else None
    
    # محاسبه نمره
    score = 0
    total = quiz.questions.count()
    for q in quiz.questions.all():
        if answers.get(q.id) == q.correct_option:
            score += 1
    final_score = (score / total) * 100 if total > 0 else 0
    
    # ثبت تلاش
    student_profile = request.user.student
    attempt = QuizAttempt.objects.create(
        student=student_profile,
        quiz=quiz,
        score=final_score
    )
    
    # پاک کردن session
    request.session.pop('quiz_questions', None)
    request.session.pop('quiz_id', None)
    request.session.pop('quiz_start_time', None)
    
    messages.success(request, f'آزمون با موفقیت ثبت شد. نمره شما: {final_score:.1f} از ۱۰۰')
    return redirect('academy:quiz_result', attempt_id=attempt.id)

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, pk=attempt_id, student__user=request.user)
    return render(request, 'academy/quiz_result.html', {'attempt': attempt})



from django.http import FileResponse, Http404
from django.core.exceptions import PermissionDenied

@login_required
def serve_pdf_inline(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    # چک دسترسی دانشجو به دوره
    if not hasattr(request.user, 'student') or content.course not in request.user.student.enrolled_courses.all():
        raise PermissionDenied()
    if not content.file or not content.file.path:
        raise Http404("فایل وجود ندارد")
    response = FileResponse(content.file.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{content.file.name}"'
    return response



