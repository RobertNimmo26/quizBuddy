from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import os
import random

from quiz.models import Quiz, Question, Option, Class, User, QuizTaker, Character
from quiz.forms import UserFormStudent, UserFormTeacher, quizCreationForm, questionFormset, QuizLibrary, classCreationForm

class dashboardTeacherViewTest(TestCase):
    def setUp(self):
        # Creating a teacher user
        charac = Character.objects.get_or_create(characterType= 1, evolutionStage = 1)[0]
        charac.save()


        test_teacher1 = User.objects.create_user(email = "teacher1@email.com", password = "1234", name = "teacher1",
                                                    username = "teacher1 ", is_teacher = True, is_staff = True )
        test_teacher1.save()
        test_student1 = User.objects.create_user(email = "student1@email.com", password = "1234", name = "student1",
                                                    username = "student1 ",is_student = True, character = charac ,evolveScore = 1 )
        test_student1.save()

        test_teacher2 = User.objects.create_user(email = "teacher2@email.com", password = "1234", name = "teacher2",
                                                    username = "teacher2 ", is_teacher = True, is_staff = True )
        test_teacher2.save()
        test_student2 = User.objects.create_user(email = "student2@email.com", password = "1234", name = "student2",
                                                    username = "student2 ",is_student = True, character = charac ,evolveScore = 1 )
        test_student2.save()

        #Creating Classes
        class1 = Class.objects.get_or_create(name= "class1")[0]
        class1.save()
        class1.student.add(User.objects.get(email = "student1@email.com"))
        class1.teacher.add(User.objects.get(email = "teacher1@email.com"))

        class2 = Class.objects.get_or_create(name= "class2")[0]
        class2.save()
        class2.student.add(User.objects.get(email = "student2@email.com"))
        class2.teacher.add(User.objects.get(email = "teacher1@email.com"))

        #Creating Quizzes
        date_time = timezone.now() + timezone.timedelta(days=5)
        get_teacher = test_teacher1

        q = Quiz.objects.get_or_create(name = "quiz1",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q.save()
        q.course.add(class1)


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("dashboardTeacher"))
        self.assertRedirects(response, "/?next=/dashboardTeacher/")

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email = "teacher1@email.com", password = "1234")
        response = self.client.get(reverse("dashboardTeacher"))

        # Logged in?
        self.assertEqual(str(response.context['user']), 'teacher1@email.com')

        #Correct template
        self.assertTemplateUsed(response, 'dashboard-teacher.html')

    def test_classes(self):
        login = self.client.login(email = "teacher1@email.com", password = "1234")
        response = self.client.get(reverse("dashboardTeacher"))

        #right Classes
        self.assertEqual(len(response.context['classes']), 2)

        for i in response.context['classes']:
            self.assertEquals(response.context['user'].email, i.get_teachers())
