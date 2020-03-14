from django import forms
from django.contrib.auth.models import User
from quiz.models import Class, Quiz,Question, Option, QuizTaker

class ReadOnlyText(forms.TextInput):
  input_type = 'text'

  def render(self, name, value, attrs=None,renderer=None):
     if value is None: 
         value = ''
     return value

class QuizTakingForm(forms.Form):
    #count =forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    countQuestions=0
    quiz = Quiz.objects.get(quizId = 1)
    print(quiz.name)
    formQuiz = forms.CharField(widget =forms.HiddenInput(),initial=quiz.name)
    question_list = Question.objects.filter(quiz = quiz)
    for index, question in enumerate(question_list):
        option_list = Option.objects.filter(question=question_list[index])
        vars()["formQuestion"+str(index)] = forms.CharField(widget =ReadOnlyText,label=question.text)
        vars()["formOption"+str(index)] = forms.ModelMultipleChoiceField(widget=forms.RadioSelect, queryset=option_list, label="",)
        countQuestions+=1
    print(countQuestions)
    count =forms.IntegerField(initial=countQuestions,widget = forms.HiddenInput())