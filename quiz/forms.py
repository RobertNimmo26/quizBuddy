from django import forms
from django.forms import formset_factory
from .models import User, Class

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
    quiz_title = forms.CharField(label="Quiz Title", max_length=50, required=True)
    quiz_description = forms.CharField(label="Quiz Description", max_length=255, required=True)

    course = forms.ModelChoiceField(queryset=Class.objects.all(),label="Class", required=True)
    due_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=True)

class questionCreationForm(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={}), label="Question", max_length=50, required=True)
    first_option = forms.CharField(widget=forms.TextInput(attrs={}), label="Option 1", max_length=50, required=True)
    second_option = forms.CharField(widget=forms.TextInput(attrs={}), label="Option 2", max_length=50, required=True)
    third_option = forms.CharField(widget=forms.TextInput(attrs={}), label="Option 3", max_length=50, required=True)
    ANSWERS=[('first_option','option 1'),
         ('second_option','option 2'),
         ('third_option', 'option 3')]
    correct_answer = forms.ChoiceField(choices=ANSWERS, widget=forms.RadioSelect(attrs={}))
# Formset Allows for adding multiple forms
questionFormset = formset_factory(questionCreationForm)


