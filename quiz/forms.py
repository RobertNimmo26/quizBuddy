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

class quizCreationForm(forms.Form):
    quiz_title = forms.CharField(label="Quiz Title:", max_length=50, required=True)
    course = forms.CharField(label="Course:", max_length=50, required=True)
    question = forms.CharField(label="Question:", max_length=50, required=True)
    first_option = forms.CharField(label="Option 1:", max_length=50, required=True)
    second_option = forms.CharField(label="Option 2:", max_length=50, required=True)
    third_option = forms.CharField(label="Option 3:", max_length=50, required=True)
    due_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=True)
    