from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    content = models.TextField(verbose_name="متن اعلان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    show_on_login = models.BooleanField(default=True, verbose_name="نمایش در صفحه لاگین")
    show_on_dashboard = models.BooleanField(default=True, verbose_name="نمایش در داشبورد")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']