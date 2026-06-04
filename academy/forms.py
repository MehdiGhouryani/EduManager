from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile

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
            # پروفایل توسط سیگنال ساخته می‌شود، فقط نقش را به روز می‌کنیم
            profile = user.profile
            profile.role = 'student'
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
        return user