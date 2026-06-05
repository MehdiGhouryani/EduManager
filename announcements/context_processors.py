from .models import Announcement

def announcement_processor(request):
    # دریافت آخرین اعلان فعال (مثلاً برای صفحه لاگین یا داشبورد)
    announcement = Announcement.objects.filter(is_active=True).first()
    return {
        'global_announcement': announcement,
        'login_announcement': Announcement.objects.filter(is_active=True, show_on_login=True).first(),
        'dashboard_announcement': Announcement.objects.filter(is_active=True, show_on_dashboard=True).first(),
    }