from django import forms
from .models import User

class UserFormStudent(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_student = forms.CharField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_student','character')

class UserFormTeacher(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, initial=True)
    is_teacher = forms.CharField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_teacher')
