from django import forms
from .models import User

#took out character (and related lines) for now as im still not sure how we're gonna do it (and also the radiobuttons are ugly af so)
class UserFormStudent(forms.ModelForm):
  
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password')

class UserFormTeacher(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), initial=True)
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password')
