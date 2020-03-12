from django import forms
from quiz.models import Question, Quiz, Option


class quizCreationForm(forms.ModelForm):
    

    # Form info
    class Meta:
        model = Quiz
        fields = ()