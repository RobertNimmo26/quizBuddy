from django.contrib import admin
from quiz.models import User, QuizTaker, Character, Quiz, Question, Class, Option

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','name','is_teacher','is_student','evolveScore')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('courseId','name','get_teachers','get_students')
    prepopulated_fields = {'slug':('courseId',)}

class QuizTakerAdmin(admin.ModelAdmin):
    list_display = ('correctAnswers','is_completed')

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('characterType','evolutionStage','can_change')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quizId', 'name', 'description', 'due_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionId','text', 'quiz')

class OptionAdmin(admin.ModelAdmin):
    list_display = ('optionId','text', 'question', 'is_correct')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Option, OptionAdmin)
