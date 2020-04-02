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

#VIEW TESTING

class registerTeacherTest(TestCase):

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("registerTeacher"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("registerTeacher"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register-teacher.html")

    def test_teacher_registration_sent(self):
        form_data = {
            'username': "A",
            'name': "A",
            'email': "a@a.com",
            'password': "aaaaaaaa",
            'is_teacher': True,
            'is_staff': True
        }
        form = UserFormTeacher()
        response = self.client.post(reverse("registerTeacher"), form_data)
        self.assertEqual(response.status_code, 200)

    def test_teacher_registration_worked(self):
        form_data = {
            'username': "A",
            'name': "A",
            'email': "a@a.com",
            'password': "aaaaaaaa",
            'is_teacher': True,
        }
        form = UserFormTeacher()
        response = self.client.post(reverse("registerTeacher"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().username, "A")
        self.assertTrue(User.objects.get().is_teacher)

class registerStudentTest(TestCase):

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("registerStudent"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("registerStudent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register-student.html")

    def test_student_registration_sent(self):
        form_data = {
            'username': "A",
            'name': "A",
            'email': "a@a.com",
            'password': "aaaaaaaa",
            'is_student': True,
        }
        form = UserFormStudent()
        response = self.client.post(reverse("registerStudent"), form_data)
        self.assertEqual(response.status_code, 200)

    def test_student_registration_worked(self):
        form_data = {
            'username': "A",
            'name': "A",
            'email': "a@a.com",
            'password': "aaaaaaaa",
            'is_student': True,
        }
        form = UserFormStudent()
        response = self.client.post(reverse("registerStudent"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().username, "A")
        self.assertTrue(User.objects.get().is_student)
        #Student has the def character - which is type 1 at evolutionStage 1
        self.assertEqual(User.objects.get().character.characterType, 1)
        self.assertEqual(User.objects.get().character.evolutionStage, 1)

class userLoginTest(TestCase):

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

class aboutTest(TestCase):

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

class manageStudentTest(TestCase):
    def setUp(self):
        test_teacher1 = User.objects.create_user(email = "teacher1@email.com", password = "1234", name = "teacher1",
                                                    username = "teacher1 ", is_teacher = True, is_staff = True )
        test_teacher1.save()
        test_student1 = User.objects.create_user(email = "student1@email.com", password = "1234", name = "student1",
                                                    username = "student1 ",is_student = True)
        test_student1.save()

        test_student2 = User.objects.create_user(email = "student2@email.com", password = "1234", name = "student2",
                                                    username = "student2 ",is_student = True)
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
        login = self.client.login(email = "teacher1@email.com", password = "1234")

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("manageStudent"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("manageStudent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manage-student.html")

    def test_shows_correct_classes(self):
        response = self.client.get(reverse("manageStudent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manage-student.html")
        self.assertEqual(len(response.context['classes']), 2)
        for i in response.context['classes']:
            self.assertEquals(response.context['user'].email, i.get_teachers())

    def test_shows_correct_students(self):
        response = self.client.get(reverse("manageStudent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manage-student.html")
        self.assertEqual(len(response.context['classes']), 2)
        for i in response.context['classes']:
            if(i.name == "class1"):
                self.assertEqual(len(response.context['classes'][i]), 1)
                self.assertEqual(response.context['classes'][i][0], "student1")
            else:
                self.assertEqual(len(response.context['classes'][i]), 1)
                self.assertEqual(response.context['classes'][i][0], "student2")

class classListTest(TestCase):

    def setUp(self):
        test_teacher1 = User.objects.create_user(email = "teacher1@email.com", password = "1234", name = "teacher1",
                                                    username = "teacher1 ", is_teacher = True, is_staff = True )
        test_teacher1.save()
        test_student1 = User.objects.create_user(email = "student1@email.com", password = "1234", name = "student1",
                                                    username = "student1 ",is_student = True)
        test_student1.save()
        test_removestudent = User.objects.create_user(email = "removestudent@email.com", password = "1234", name = "removestudent",
                                                    username = "removestudent",is_student = True)
        test_removestudent.save()

        #student to be added - hence we don't add them to the class yet
        test_addstudent = User.objects.create_user(email = "addstudent@email.com", password = "1234", name = "addstudent",
                                                    username = "addstudent",is_student = True)
        test_addstudent.save()

        #Creating Classes
        class1 = Class.objects.get_or_create(name= "class1")[0]
        class1.save()
        class1.student.add(User.objects.get(email = "student1@email.com"))
        class1.student.add(User.objects.get(email = "removestudent@email.com"))
        class1.teacher.add(User.objects.get(email = "teacher1@email.com"))

        login = self.client.login(email = "teacher1@email.com", password = "1234")

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("classList", args=["1"]))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("classList", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classList.html")

    def test_user_does_not_exist(self):
        data = {
            'button': "add",
            'add_student': "notexist@notexist.com",
            }
        response = self.client.post(reverse("classList", args=["1"]), data)
        self.assertTrue(response.context["remove_error"])

    def test_remove_student(self):
        form_data = {
            'button': "removestudent@email.com",
            }
        self.assertEqual(Class.objects.get(courseId=1).student.all().count(),2)
        response = self.client.post(reverse("classList", args=["1"]), form_data)
        self.assertEqual(Class.objects.get(courseId=1).student.all().count(),1)
        self.assertEqual(User.objects.get(email = "removestudent@email.com") in response.context['students'], False)
        #adding back the student we just removed
        student = User.objects.filter(email="removestudent@email.com").get()
        student.students.add(Class.objects.get(slug=1))

    def test_add_student(self):
        form_data = {
            'button': "add",
            'add_student': "addstudent@email.com",
            }
        self.assertEqual(Class.objects.get(courseId=1).student.all().count(),2)
        response = self.client.post(reverse("classList", args=["1"]), form_data)
        self.assertEqual(Class.objects.get(courseId=1).student.all().count(),3)
        self.assertTrue(User.objects.get(email = "addstudent@email.com") in response.context['students'])
        #removing the student we just added
        student = User.objects.filter(email="addstudent@email.com").get()
        student.students.remove(Class.objects.get(slug=1))

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


class show_classTeacherViewTest(TestCase):
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



        q1 = Quiz.objects.get_or_create(name = "quiz2",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q1.save()
        q1.course.add(class1)

        q2 = Quiz.objects.get_or_create(name = "quiz3",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q2.save()
        q2.course.add(class1)

    def test_redirect_if_not_logged_in_Class(self):
        response = self.client.get(reverse("classTeacher", args=["1"]))
        self.assertRedirects(response, "/?next=/dashboardTeacher/classTeacher/1/")

    def test_logged_in_uses_correct_template_Class(self):
        login = self.client.login(email = "teacher1@email.com", password = "1234")
        response = self.client.get(reverse("classTeacher", args=["1"]))

        # Logged in?
        self.assertEqual(str(response.context['user']), 'teacher1@email.com')

        #Correct template
        self.assertTemplateUsed(response, 'classTeacher.html')

    def test_classes_Class(self):
        login = self.client.login(email = "teacher1@email.com", password = "1234")
        response = self.client.get(reverse("classTeacher", args=["1"]))

        #right Classes
        self.assertEqual(len(response.context['classes']), 2)

        for i in response.context['classes']:
            self.assertEquals(response.context['user'].email, i.get_teachers())

        self.assertEquals(response.context['user'].email, response.context['class'].get_teachers())

    def test_got_all_quizzes(self):
        login = self.client.login(email = "teacher1@email.com", password = "1234")
        response = self.client.get(reverse("classTeacher", args=["1"]))

        self.assertEqual(len(response.context['quizzes']), 3)

        for q in response.context['quizzes']:
            self.assertEquals(response.context['class'].courseId, q.course.get().courseId)


class show_classStudentViewTest(TestCase):
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
        class2.student.add(User.objects.get(email = "student1@email.com"))
        class2.teacher.add(User.objects.get(email = "teacher1@email.com"))

        #Creating Quizzes
        date_time = timezone.now() + timezone.timedelta(days=5)
        get_teacher = test_teacher1

        q = Quiz.objects.get_or_create(name = "quiz1",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q.save()
        q.course.add(class1)



        q1 = Quiz.objects.get_or_create(name = "quiz2",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q1.save()
        q1.course.add(class1)

        q2 = Quiz.objects.get_or_create(name = "quiz3",description="quiz1",due_date=date_time,question_count=3, teacher=get_teacher)[0]
        q2.save()
        q2.course.add(class1)

    def test_redirect_if_not_logged_in_Class(self):
        response = self.client.get(reverse("classStudent", args=["1"]))
        self.assertRedirects(response, "/?next=/dashboardStudent/classStudent/1/")

    def test_logged_in_uses_correct_template_Class(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.get(reverse("classStudent", args=["1"]))

        # Logged in?
        self.assertEqual(str(response.context['user']), 'student1@email.com')

        #Correct template
        self.assertTemplateUsed(response, 'classStudent.html')

    def test_classes_Class(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.get(reverse("classStudent", args=["1"]))

        #right Classes
        self.assertEqual(len(response.context['classes']), 2)

        for i in response.context['classes']:
            self.assertEquals(response.context['user'].email, i.get_students())

        self.assertEquals(response.context['user'].email, response.context['class'].get_students())


    def test_got_all_quizzes(self):
        login = self.client.login(email = "student1@email.com", password = "1234")
        response = self.client.get(reverse("classStudent", args=["1"]))

        self.assertEqual(len(response.context['quizzes']), 3)

        for q in response.context['quizzes']:
            self.assertEquals(response.context['class'].courseId, q.course.get().courseId)
