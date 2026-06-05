from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # مهم: نگهداری لاگین
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'لطفاً خطاها را اصلاح کنید.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})