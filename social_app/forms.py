from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comment,Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napisz post!'}), label='')
    class Meta:
        model = Post
        fields = ('description','image')

class CommentForm(forms.ModelForm):
    value = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napisz komentarz!'}), label='')
    class Meta:
        model = Comment
        fields = ('value',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
