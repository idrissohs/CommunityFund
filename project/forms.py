from django import forms
from django.contrib.auth.models import User
from .models import Project, Match

#form to collect user data
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

#form to collect project data
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'about',)

#form to collect matching data
class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ('funding',)
