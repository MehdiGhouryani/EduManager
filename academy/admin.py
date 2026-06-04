from django.contrib import admin
from .models import Course, Student, Content


class ContentInline(admin.TabularInline):
    """
    این کلاس اجازه می‌دهد محتواها مستقیماً داخل فرم ویرایش دوره
    نمایش داده و مدیریت شوند.
    """
    model = Content
    extra = 0  # فرم اضافی خالی نشان نده
    fields = ['title', 'content_type', 'file', 'text_content', 'order', 'duration']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست دوره‌ها نمایش داده می‌شوند
    list_display = ['title', 'instructor', 'start_date', 'end_date', 'is_active', 'is_full_display']

    # فیلترهای سمت راست صفحه لیست
    list_filter = ['is_active', 'start_date']

    # جستجوی متنی
    search_fields = ['title', 'instructor']

    # پر شدن خودکار فیلد slug از روی title
    prepopulated_fields = {'slug': ('title',)}

    # اضافه کردن مدیریت محتواها در همان صفحه دوره
    inlines = [ContentInline]

    @admin.display(description='ظرفیت تکمیل؟', boolean=True)
    def is_full_display(self, obj):
        """وضعیت تکمیل ظرفیت را با آیکون نشان می‌دهد"""
        return obj.is_full()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # ستون‌های نمایشی
    list_display = ['full_name', 'email', 'phone', 'registered_at', 'is_active']

    # فیلتر
    list_filter = ['is_active']

    # جستجو (می‌توان بر اساس نام، ایمیل و ... جستجو کرد)
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

    # انتخاب آسان‌تر دوره‌ها (باکس افقی)
    filter_horizontal = ['enrolled_courses']

    # اکشن‌های گروهی سفارشی
    actions = ['deactivate_students', 'activate_students']

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'نام کامل'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'ایمیل'

    @admin.action(description='غیرفعال‌سازی دانشجویان انتخاب‌شده')
    def deactivate_students(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} دانشجو غیرفعال شد.')

    @admin.action(description='فعال‌سازی دانشجویان انتخاب‌شده')
    def activate_students(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} دانشجو فعال شد.')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'uploaded_at']
    list_filter = ['content_type', 'course']
    search_fields = ['title']