from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent = Notification.objects.filter(user=request.user)[:5]
        return {'unread_count': count, 'recent_notifications': recent}
    return {'unread_count': 0, 'recent_notifications': []}