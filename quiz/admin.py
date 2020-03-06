from django.contrib import admin
from quiz.models import User,QuizTaker,Character, Quiz, Question

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','name','is_teacher','is_student')

class QuizTakerAdmin(admin.ModelAdmin):
    list_display = ('correctAnswers','is_completed')

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('characterType','evolutionStage','evolveScore')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'due_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
