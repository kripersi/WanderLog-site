from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'hidden-input'})
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}),
        max_length=5000
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
