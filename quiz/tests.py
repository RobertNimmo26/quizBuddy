from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import os
import random

from quiz.models import Quiz, Question, Option, Class, User, QuizTaker, Character

from quiz.forms import UserFormStudent, UserFormTeacher, quizCreationForm, questionFormset, QuizLibrary, classCreationForm
from quiz.models import Character,User,Class, Quiz, Question, Option, QuizTaker
from quiz.managers import CustomUserManager
import random

#FORM TESTING - based on https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class UserFormStudentTest(TestCase):
    def test_password_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_username_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'User name')

    def test_name_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')

    def test_email_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email address')

class UserFormTeacherTest(TestCase):
    def test_password_label(self):
        form = UserFormTeacher()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_username_label(self):
        form = UserFormTeacher()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'User name')

    def test_name_label(self):
        form = UserFormTeacher()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')

    def test_email_label(self):
        form = UserFormTeacher()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email address')

class classCreationFormTest(TestCase):
    def test_name_label(self):
        form = classCreationForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')

class quizCreationFormTest(TestCase):
    def test_quiz_title_label(self):
        form = quizCreationForm()
        self.assertTrue(form.fields['quiz_title'].label == None or form.fields['quiz_title'].label == 'Quiz Title')

    def test_quiz_description_label(self):
        form = quizCreationForm()
        self.assertTrue(form.fields['quiz_description'].label == None or form.fields['quiz_description'].label == 'Quiz Description')

    def test_course_label(self):
        form = quizCreationForm()
        self.assertTrue(form.fields['course'].label == None or form.fields['course'].label == 'Class')

    def test_course_queryset(self):
        classVar = Class.objects.get_or_create(name="C")[0]
        classVar.save()
        form = quizCreationForm()
        self.assertTrue(form.fields['course'].queryset.get() == classVar)

    def test_due_date_label(self):
        form = quizCreationForm()
        self.assertTrue(form.fields['due_date'].label == None or form.fields['due_date'].label == 'Quiz Description')

class QuizLibraryTest(TestCase):
    def test_quiz_label(self):
        form = QuizLibrary()
        self.assertTrue(form.fields['quiz'].label == None or form.fields['quiz'].label == 'Quiz')

    def test_quiz_queryset(self):
        randomDay=random.randint(-5,20)
        due_date = timezone.now() + timezone.timedelta(days=randomDay)
        teacher = User.objects.create_user(email = "a@a.com", password = "aaaaaaaa", name = "a", username = "a", is_teacher = True, is_staff = True )
        teacher.save()
        quiz = Quiz(name = "A",description="A",due_date=due_date,question_count=2,teacher=teacher)
        quiz.save()
        form = QuizLibrary()
        self.assertTrue(form.fields['quiz'].queryset.get() == quiz)

    def test_course_label(self):
        form = QuizLibrary()
        self.assertTrue(form.fields['course'].label == None or form.fields['course'].label == 'Class')

    def test_course_queryset(self):
        classVar = Class.objects.get_or_create(name="C")[0]
        classVar.save()
        form = QuizLibrary()
        self.assertTrue(form.fields['course'].queryset.get() == classVar)

    def test_due_date_label(self):
        form = QuizLibrary()
        self.assertTrue(form.fields['due_date'].label == None or form.fields['due_date'].label == 'Due date')



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


class dashboardStudentViewTest(TestCase):
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
            response = self.client.get(reverse("dashboardStudent"))
            self.assertRedirects(response, "/?next=/dashboardStudent/")

        def test_logged_in_uses_correct_template(self):
            login = self.client.login(email = "student1@email.com", password = "1234")
            response = self.client.get(reverse("dashboardStudent"))

            # Logged in?
            self.assertEqual(str(response.context['user']), 'student1@email.com')

            #Correct template
            self.assertTemplateUsed(response, 'dashboard-student.html')

class preferencesStudentViewTest(TestCase):
    def setUp(self):
        charac1 = Character.objects.get_or_create(characterType= 1, evolutionStage = 1)[0]
        charac1.save()

        charac2 = Character.objects.get_or_create(characterType= 1, evolutionStage = 1)[0]
        charac2.save()

        test_student1 = User.objects.create_user(email = "student1@email.com", password = "1234", name = "student1",
                                                    username = "student1 ",is_student = True, character = charac1 ,evolveScore = 1 )
        test_student1.save()

        test_student2 = User.objects.create_user(email = "student2@email.com", password = "1234", name = "student2",
                                                            username = "student2 ",is_student = True, character = charac2 ,evolveScore = 10 )
        test_student2.save()

    def test_username_changed_and_redirected_to_dashboard(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.post(reverse('preferencesStudent'), {'username': 'Billy12'})
        #302 indicates an update
        self.assertEqual(response.status_code, 302)
        #after updating something, user is redirected to the dashboard
        after_redirect_response = self.client.get(reverse('dashboardStudent'))
        self.assertEqual(after_redirect_response.context['user'].username, 'Billy12')
    
    def test_name_changed_and_redirected_to_dashboard(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.post(reverse('preferencesStudent'), {'name': 'Billy'})
        self.assertEqual(response.status_code, 302)
        after_redirect_response = self.client.get(reverse('dashboardStudent'))
        self.assertEqual(after_redirect_response.context['user'].name, 'Billy')

    def test_email_changed_and_redirected_to_dashboard(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.post(reverse('preferencesStudent'), {'email':'billy@gla.ac.uk'})
        self.assertEqual(response.status_code, 302)
        after_redirect_response = self.client.get(reverse('dashboardStudent'))
        self.assertEqual(after_redirect_response.context['user'].email, 'billy@gla.ac.uk')

    def test_password_changed_and_user_logged_out(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.post(reverse('preferencesStudent'), {'password': '5698'})
        #302 indicates that password has been updates
        self.assertEqual(response.status_code, 302)
        #update was successful so user should have been logged out
        after_redirect_response = self.client.get(reverse('dashboardStudent'))
        self.assertRedirects(response, "/")


                               



