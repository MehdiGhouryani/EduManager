from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from .models import Student   # <-- اضافه شد

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.role = 'student'
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
            # 👇 ایجاد مدل Student برای این کاربر
            Student.objects.get_or_create(user=user)
        return user


# بقیه فرم‌های Quiz و Question (بدون تغییر)
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'time_limit': forms.NumberInput(attrs={'min': 0, 'placeholder': 'دقیقه (اختیاری)'})
        }
        labels = {
            'title': 'عنوان آزمون',
            'description': 'توضیحات',
            'time_limit': 'زمان مجاز (دقیقه)',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
            'option1': forms.TextInput(attrs={'class': 'form-control'}),
            'option2': forms.TextInput(attrs={'class': 'form-control'}),
            'option3': forms.TextInput(attrs={'class': 'form-control'}),
            'option4': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(choices=[(1,'گزینه ۱'),(2,'گزینه ۲'),(3,'گزینه ۳'),(4,'گزینه ۴')])
        }





from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='مرا به خاطر بسپار', widget=forms.CheckboxInput)