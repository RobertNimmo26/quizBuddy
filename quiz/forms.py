from django import forms
from .models import User

#took out character (and related lines) for now as im still not sure how we're gonna do it (and also the radiobuttons are ugly af so)
class UserFormStudent(forms.ModelForm):
    #CHAR_CHOICES =(("1", "Char1"), ("2", "Char2"), ("3", "Char3"))
    password = forms.CharField(widget=forms.PasswordInput())
    #character = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHAR_CHOICES)
    #is_student = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password')

class UserFormTeacher(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), initial=True)
    #is_teacher = forms.BooleanField(widget=forms.HiddenInput(),required=False, initial=True)
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password')
