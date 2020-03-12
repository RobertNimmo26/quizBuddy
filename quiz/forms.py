from django import forms
from django.forms import formset_factory
from quiz.models import Question, Quiz, Option

class questionForm(forms.ModelForm):
    questionName = forms.CharField(max_length=50, required=True)

class quizForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=255, required=False)
    due_date = forms.DateTimeField(required=True)
    question_count = forms.IntegerField(default=0)
   
    class Meta:
       model = Quiz
       fields = ('name', 'description', 'due_date')
       
class quizCreationForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ()