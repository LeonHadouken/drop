from authentication.forms import UserEditForm, ProfileForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import Profile
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

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
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    # Инициализируем формы
    user_form = UserEditForm(instance=user)
    profile_form = ProfileForm(instance=profile)
    password_form = CustomPasswordChangeForm(user)

    active_tab = request.GET.get('tab', 'user-data')  # Получаем активную вкладку из GET-параметра

    # Обрабатываем POST-запрос
    if request.method == 'POST':
        if 'user_data' in request.POST:  # Если отправлена форма данных пользователя
            user_form = UserEditForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('edit_profile') + '?tab=user-data'

        elif 'avatar' in request.POST:  # Если отправлена форма аватара
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('edit_profile') + '?tab=avatar'

        elif 'password' in request.POST:  # Если отправлена форма пароля
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Оставляем пользователя в системе
                return redirect('edit_profile') + '?tab=password'

    # Передаём все формы в шаблон
    return render(request, 'profile/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'active_tab': active_tab,  # Передаем активную вкладку для подсветки
    })

def edit_user_data(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/edit.html', {
        'form': user_form,
        'profile_form': profile_form,
        'password_form': CustomPasswordChangeForm(request.user),  # Для пароля
    })

def edit_avatar(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('edit')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/edit.html', {
        'profile_form': profile_form,
        'form': UserEditForm(instance=request.user),  # Для данных пользователя
        'password_form': CustomPasswordChangeForm(request.user),  # Для пароля
    })

def edit_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('edit')
    else:
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'profile/edit.html', {
        'password_form': password_form,
        'form': UserEditForm(instance=request.user),  # Для данных пользователя
        'profile_form': ProfileForm(instance=request.user.profile),  # Для аватара
    })

