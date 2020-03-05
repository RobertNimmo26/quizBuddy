from django.contrib import admin
from quiz.models import *

# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'due_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    
# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)