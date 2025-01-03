from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from django import forms
from django.contrib.auth.models import User

# Форма для редактирования личных данных пользователя
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # Переопределение меток и подсказок для полей формы
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

# Форма для регистрации пользователя с аватаром
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес электронной почты'})
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    avatar = forms.ImageField(
        label="Аватар",
        required=False,  # Сделать необязательным, чтобы можно было регистрироваться без аватара
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Настройка полей username, password1 и password2
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Обязательно. До 150 символов. Только буквы, цифры и символы @/./+/-/_.</small>'
            '</span>'
        )

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Ваш пароль не должен быть похож на вашу личную информацию.</li>'
            '<li>Ваш пароль должен содержать не менее 8 символов.</li>'
            '<li>Ваш пароль не должен быть распространённым.</li>'
            '<li>Ваш пароль не должен состоять только из цифр.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['password2'].label = 'Подтвердите пароль'
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Введите тот же пароль, что и выше, для подтверждения.</small>'
            '</span>'
        )

# Форма для редактирования аватара
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Переопределение метки для поля аватар
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

# Форма для изменения пароля
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Переопределение меток и подсказок для полей формы
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение нового пароля'
        self.fields['old_password'].help_text = 'Введите ваш текущий пароль.'
        self.fields['new_password1'].help_text = 'Введите новый пароль.'
        self.fields['new_password2'].help_text = 'Подтвердите новый пароль.'
