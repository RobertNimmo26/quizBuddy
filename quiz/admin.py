from django.contrib import admin
from quiz.models import User,QuizTaker,Character

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','name','is_teacher','is_student')

class QuizTakerAdmin(admin.ModelAdmin):
    list_display = ('correctAnswers','is_completed')

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('characterType','evolutionStage','evolveScore')



# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(Character, CharacterAdmin)