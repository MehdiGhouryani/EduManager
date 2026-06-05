from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification, EventType

@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    """پس از ایجاد کاربر جدید، یک اعلان خوش‌آمدگویی برای او ارسال کن"""
    if created:
        event, _ = EventType.objects.get_or_create(name='user_registration')
        Notification.objects.create(
            user=instance,
            event_type=event,
            message="به جمع دانشجویان ما خوش آمدید! از اینکه به ما پیوستید خوشحالیم.",
            link="/dashboard/"
        )