from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class Character(models.Model):
    characterType = models.IntegerField(_("type"))
    evolutionStage = models.IntegerField(_("stage"),default=1)
    evolveScore = models.IntegerField(_("score"),default=0)

class QuizTaker(models.Model):
    #user = models.ForeignKey("User", on_delete=models.CASCADE) #---Need to connect
    #quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE) #---Need to connect
    correctAnswers = models.IntegerField(_("correct answers"))
    is_completed = models.BooleanField(_("completed"))
    #timestamp = models.models.DateTimeField(auto_now_add=True, blank=True)


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