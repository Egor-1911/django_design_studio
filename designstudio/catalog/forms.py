from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DesignRequest

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        widget=forms.TextInput(),
    )
    username = forms.CharField(
        max_length=150,
        label="Логин",
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        label="Почта",
        widget=forms.EmailInput()
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput()
    )

    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Вы должны согласиться на обработку персональных данных.'}
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn’t match.")
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
            raise ValidationError('Это поле обязательно для заполнения.')
        return name.strip()
