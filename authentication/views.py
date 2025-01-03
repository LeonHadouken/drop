from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            # Устанавливаем поля по умолчанию для профиля
            is_premium = False  # По умолчанию - не премиум
            is_moderator = False  # По умолчанию - не модератор

            # Создаем профиль с указанными значениями
            Profile.objects.create(
                user=user,
                is_premium=is_premium,
                is_moderator=is_moderator
            )

            # Аутентификация и вход в систему
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "Вы успешно зарегистрировались! Добро пожаловать!")
            return redirect('index')
        else:
            messages.error(request, "Ошибка регистрации. Пожалуйста, попробуйте снова.")
    else:
        form = SignUpForm()

    return render(request, 'auth/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')