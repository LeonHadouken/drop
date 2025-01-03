from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from authentication.models import Profile

def index(request):
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		# Проверка, существует ли пользователь с таким именем
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None

		if user is None:
			# Если пользователя нет в базе данных, выводим сообщение
			messages.error(request, "Пользователь с таким именем не найден.")
			return redirect('index')

		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Вход выполнен!")
			return redirect('index')
		else:
			messages.error(request, "Неверный логин или пароль. Попробуйте снова.")
			return redirect('index')
	else:
		return render(request, 'index.html')


def logout_user(request):
	logout(request)
	messages.success(request, "Вы вышли из учетной записи.")
	return redirect('index')


@login_required
def profile(request):
	user = request.user
	try:
		profile = Profile.objects.get(user=user)
	except Profile.DoesNotExist:
		profile = None

	return render(request, 'profile.html', {
		'user': user,
		'profile': profile
	})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserChangeForm(instance=request.user)

    # Если не суперпользователь, ограничиваем доступ к полям
    if not request.user.is_superuser:
        # Выбираем поля, которые можно редактировать
        form.fields['username'].widget.attrs['readonly'] = True  # Имя пользователя только для чтения
        form.fields['email'].widget.attrs['readonly'] = True  # Почта только для чтения
        form.fields['password'].widget.attrs['readonly'] = True  # Пароль только для чтения

    return render(request, 'edit_profile.html', {'form': form})