from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DesignRequest
import re
import os


class RegistrationForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100, widget=forms.TextInput())
    username = forms.CharField(max_length=150, label="Логин", widget=forms.TextInput())
    email = forms.EmailField(label="Почта", widget=forms.EmailInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())
    consent = forms.BooleanField(label='Согласие на обработку персональных данных', required=True, error_messages={'required': 'Согласие обязательно'})

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not full_name:
            raise ValidationError('ФИО обязательно для заполнения.')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', full_name):
            raise ValidationError('ФИО может содержать только кириллические буквы, пробелы и дефис.')
        return full_name.strip()

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise ValidationError('Логин обязателен.')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин может содержать только латинские буквы и дефис.')
        if len(username) < 3:
            raise ValidationError('Логин должен содержать не менее 3 символов.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует. Введите другой логин')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Email обязателен.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Эта почта уже зарегистрирована. Используйте другую')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise ValidationError('Пароль обязателен.')
        if len(password1) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise ValidationError('Подтверждение пароля обязательно.')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user





class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['name', 'category', 'room_type', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название заявки'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 10, 'placeholder': 'Пожелания к дизайну'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Название заявки',
            'room_type': 'Тип помещения',
            'description': 'Описание дизайна',
            'image': 'Фото помещения или планировки',
            'category': 'Категория заявки',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError('Обязательное полея')
        return name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise ValidationError('Обязательное поле')
        return description.strip()

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError('Обязательный выбор')
        return category

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError('Фото помещения или план обязательны для загрузки.')
        if image.size > 2 * 1024 * 1024:
            raise ValidationError('Размер файла не должен превышать 2 МБ.')
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError('Прикрепите фотографию')

        return image
