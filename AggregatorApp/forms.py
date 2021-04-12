from django import forms
from django.forms import ModelForm
from .models import Profile, Comment
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'gender', 'bio', 'country')
        widgets = {'birth_date': DateInput()}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
