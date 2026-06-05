from django import forms
from academy.models import Course, Content

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'capacity', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'content_type', 'file', 'text_content', 'order', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
        }
        labels = {
            'title': 'عنوان محتوا',
            'content_type': 'نوع محتوا',
            'file': 'فایل (PDF/ویدئو)',
            'text_content': 'متن محتوا',
            'order': 'ترتیب نمایش',
            'duration': 'مدت زمان (برای ویدئو)',
        }