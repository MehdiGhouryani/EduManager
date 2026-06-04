from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان دوره")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="نامک")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    instructor = models.CharField(max_length=100, verbose_name="مدرس")
    capacity = models.PositiveIntegerField(default=30, verbose_name="ظرفیت")
    start_date = models.DateField(null=True, blank=True, verbose_name="تاریخ شروع")
    end_date = models.DateField(null=True, blank=True, verbose_name="تاریخ پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return self.title

    def is_full(self):
        """بررسی می‌کند که آیا ظرفیت دوره تکمیل شده است"""
        return self.students.count() >= self.capacity


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    phone = models.CharField(max_length=15, blank=True, verbose_name="شماره تماس")
    enrolled_courses = models.ManyToManyField(
        Course,
        related_name='students',
        blank=True,
        verbose_name="دوره‌های ثبت‌نام شده"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_full_name(self):
        return self.user.get_full_name()


class Content(models.Model):
    CONTENT_TYPES = [
        ('PDF', 'PDF'),
        ('Video', 'ویدئو'),
        ('Text', 'متن'),
    ]
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name="دوره"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان محتوا")
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='PDF', verbose_name="نوع محتوا")
    file = models.FileField(upload_to='contents/%Y/%m/', blank=True, null=True, verbose_name="فایل")
    text_content = models.TextField(blank=True, verbose_name="محتوای متنی")
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب")
    duration = models.DurationField(null=True, blank=True, verbose_name="مدت زمان (برای ویدئو)")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ بارگذاری")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    



class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/%Y/%m/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['assignment', 'student']  # هر دانشجو فقط یک بار می‌تواند ارسال کند

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit = models.PositiveIntegerField(help_text="زمان به دقیقه", null=True, blank=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'گزینه ۱'), (2, 'گزینه ۲'), (3, 'گزینه ۳'), (4, 'گزینه ۴')])

class QuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)