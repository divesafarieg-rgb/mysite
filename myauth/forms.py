from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=500, label="О себе")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата рождения")
    phone_number = forms.CharField(max_length=15, required=False, label="Телефон")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            user.email = self.cleaned_data.get('email')
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.save()

            if hasattr(user, 'profile'):
                profile = user.profile
                profile.bio = self.cleaned_data.get('bio', '')
                profile.birth_date = self.cleaned_data.get('birth_date')
                profile.phone_number = self.cleaned_data.get('phone_number', '')
                profile.save()

        return user

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First name")
    last_name = forms.CharField(max_length=30, required=False, label="Last name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'phone_number', 'avatar')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)

        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()
            profile.save()

        return profile