from django.db import models
from django.conf import settings
from academy.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignment_items'   # یکتا، با 'assignments' و 'quizzes' و 'contents' تداخل ندارد
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['-due_date']


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submission_files'
    )
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    is_late = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.assignment.due_date and self.submitted_at and self.submitted_at > self.assignment.due_date:
            self.is_late = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    class Meta:
        unique_together = ['assignment', 'student']