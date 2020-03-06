from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone

from .managers import CustomUserManager

class Character(models.Model):
    characterType = models.IntegerField(_("type"))
    evolutionStage = models.IntegerField(_("stage"),default=1)
    evolveScore = models.IntegerField(_("score"),default=0)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("user name"), max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_("name"), max_length=40)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    character = models.ForeignKey("Character", blank=True, null=True, on_delete=models.SET_NULL) #---Need to connect

    #Required django User fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #####

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Quiz Model
class Quiz(models.Model):
    name = models.CharField(unique=True, max_length=50)
    # Course represents class model
    course = models.ManyToManyField(Class)
    description = models.CharField(max_length=255)
    due_date = models.DateTimeField(auto_now_add=False)
    question_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        # Fix pluralization of model name
        verbose_name_plural = 'Quizzes'
    
# Question model
class Question(models.Model):
    text = models.CharField(unique=True, max_length=50)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.text
    
# Option Model
class Option(models.Model):
    text = models.CharField(unique=True, max_length=50)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# QuizTaker model
class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correctAnswers = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.user
