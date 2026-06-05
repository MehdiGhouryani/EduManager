from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    # علامت‌گذاری همه به عنوان خوانده شده (اختیاری)
    if request.GET.get('mark_read'):
        notifications.update(is_read=True)
    return render(request, 'notifications/list.html', {'notifications': notifications})