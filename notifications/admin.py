from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Notification, EventType

def send_notification_action(modeladmin, request, queryset):
    if 'apply' in request.POST:
        message_text = request.POST.get('notification_message')
        link = request.POST.get('notification_link', '')
        event_name = request.POST.get('event_type', 'admin_announcement')

        if not message_text:
            messages.error(request, "لطفاً متن پیام را وارد کنید.")
            return

        event, _ = EventType.objects.get_or_create(name=event_name)

        notifications = []
        for user in queryset:
            notifications.append(Notification(
                user=user,
                event_type=event,
                message=message_text,
                link=link
            ))
        Notification.objects.bulk_create(notifications)
        messages.success(request, f"پیام برای {len(notifications)} کاربر ارسال شد.")
        return HttpResponseRedirect(request.get_full_path())

    return render(request, 'admin/send_notification.html', {'users': queryset})

send_notification_action.short_description = "ارسال اعلان به کاربران انتخاب شده"

class CustomUserAdmin(UserAdmin):
    actions = [send_notification_action]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)