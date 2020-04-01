from django.test import TestCase
from django.utils import timezone
from quiz.forms import UserFormStudent, UserFormTeacher, quizCreationForm, questionFormset, QuizLibrary, classCreationForm
from quiz.models import Character,User,Class, Quiz, Question, Option, QuizTaker
from quiz.managers import CustomUserManager
from datetime import datetime
import random

#FORM TESTING - based on https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class UserFormStudentTest(TestCase):
    def test_password_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['password'].label == None or form.fields['password'].label == 'Password')

    def test_username_label(self):
        form = UserFormStudent()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Username')

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
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Username')

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

#MODEL TESTING
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        User.objects.create(username='TestUser1', email='testuser@test.com', name='Bob', is_student=True,character=character)

    def test_username_label(self):
        user = User.objects.get(email='testuser@test.com')
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_username_length(self):
        user = User.objects.get(email='testuser@test.com')
        max_length = user._meta.get_field('username').max_length
        self.assertEquals(max_length, 50)

    def test_name_label(self):
        user = User.objects.get(email='testuser@test.com')
        field_label = user._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        user = User.objects.get(email='testuser@test.com')
        max_length = user._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_email_label(self):
        user = User.objects.get(email='testuser@test.com')
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email address')

    def test_email_unique(self):
        user = User.objects.get(email='testuser@test.com')
        unique = user._meta.get_field('email').unique
        self.assertEquals(unique, True)

    def test_evolveScore_label(self):
        user = User.objects.get(email='testuser@test.com')
        field_label = user._meta.get_field('evolveScore').verbose_name
        self.assertEquals(field_label, 'score')

    def test_object_name_is_email(self):
        user = User.objects.get(email='testuser@test.com')
        expected_object_name = f'{user.email}'
        self.assertEquals(expected_object_name, str(user))

class ClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        student=User.objects.create(username='TestUserStudent', email='testsuser@test.com', name='Bobs', is_student=True,character=character)
        teacher=User.objects.create(username='TestUserTeacher', email='testtuser@test.com', name='Bobt', is_teacher=True)
        course=Class.objects.create(name='TestClass')
        course.teacher.add(teacher)
        course.student.add(student)
        course.save()

    def test_courseId_label(self):
        course = Class.objects.get(courseId=1)
        field_label = course._meta.get_field('courseId').verbose_name
        self.assertEquals(field_label, 'id')

    def test_name_label(self):
        course = Class.objects.get(courseId=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_length(self):
        course = Class.objects.get(courseId=1)
        max_length = course._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)


    def test_courseId_label(self):
        course = Class.objects.get(courseId=1)
        field_label = course._meta.get_field('teacher').verbose_name
        self.assertEquals(field_label, 'teacher')
    
    def test_teacher_label(self):
        course = Class.objects.get(courseId=1)
        field_label = course._meta.get_field('student').verbose_name
        self.assertEquals(field_label, 'student')

    def test_student_label(self):
        course = Class.objects.get(courseId=1)
        field_label = course._meta.get_field('teacher').verbose_name
        self.assertEquals(field_label, 'teacher')

    def test_get_teachers(self):
        course = Class.objects.get(courseId=1)
        teacher = User.objects.get(email='testtuser@test.com')
        self.assertEquals(course.get_teachers(), str(teacher))
    
    def test_get_students(self):
        course = Class.objects.get(courseId=1)
        student = User.objects.get(email='testsuser@test.com')
        self.assertEquals(course.get_students(), str(student))

    def test_object_name_is_name(self):
        course = Class.objects.get(courseId=1)
        expected_object_name = f'{course.name}'
        self.assertEquals(expected_object_name, str(course))
    
    def test_save(self):
        course = Class.objects.get(courseId=1)
        self.assertEquals(course.slug, str(course.courseId))
    
class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        student=User.objects.create(username='TestUserStudent', email='testsuser@test.com', name='Bobs', is_student=True,character=character)
        teacher=User.objects.create(username='TestUserTeacher', email='testtuser@test.com', name='Bobt', is_teacher=True)
        course=Class.objects.create(name='TestClass')
        course.teacher.add(teacher)
        course.student.add(student)
        course.save()
        quiz=Quiz.objects.create(name="TestQuiz",teacher=teacher,description="Test quiz model",due_date=timezone.now())
        quiz.course.add(course)
        quiz.save()

    def test_quizId_label(self):
        quiz = Quiz.objects.get(quizId=1)
        field_label = quiz._meta.get_field('quizId').verbose_name
        self.assertEquals(field_label, 'id')

    def test_name_length(self):
        quiz = Quiz.objects.get(quizId=1)
        max_length = quiz._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)
    
    def test_name_label(self):
        quiz = Quiz.objects.get(quizId=1)
        field_label = quiz._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_length(self):
        quiz = Quiz.objects.get(quizId=1)
        max_length = quiz._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_description_label(self):
        quiz = Quiz.objects.get(quizId=1)
        field_label = quiz._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')
    
    def test_due_date_autoadd(self):
        quiz = Quiz.objects.get(quizId=1)
        auto_now_add = quiz._meta.get_field('due_date').auto_now_add
        self.assertEquals(auto_now_add, False)

    def test_due_date_label(self):
        quiz = Quiz.objects.get(quizId=1)
        field_label = quiz._meta.get_field('due_date').verbose_name
        self.assertEquals(field_label, 'due date')

    def test_question_count_label(self):
        quiz = Quiz.objects.get(quizId=1)
        field_label = quiz._meta.get_field('question_count').verbose_name
        self.assertEquals(field_label, 'question count')

    def test_object_name_is_name(self):
        quiz = Quiz.objects.get(quizId=1)
        expected_object_name = f'{quiz.name}'
        self.assertEquals(expected_object_name, str(quiz))

    def test_save(self):
        quiz = Quiz.objects.get(quizId=1)
        self.assertEquals(quiz.slug, str(quiz.quizId))

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        student=User.objects.create(username='TestUserStudent', email='testsuser@test.com', name='Bobs', is_student=True,character=character)
        teacher=User.objects.create(username='TestUserTeacher', email='testtuser@test.com', name='Bobt', is_teacher=True)
        course=Class.objects.create(name='TestClass')
        course.teacher.add(teacher)
        course.student.add(student)
        course.save()
        quiz=Quiz.objects.create(name="TestQuiz",teacher=teacher,description="Test quiz model",due_date=timezone.now())
        quiz.course.add(course)
        quiz.save()
        Question.objects.create(text="QuestionText", quiz=quiz)

    def test_questionId_label(self):
        question = Question.objects.get(questionId=1)
        field_label = question._meta.get_field('questionId').verbose_name
        self.assertEquals(field_label, 'id')

    def test_text_length(self):
        question = Question.objects.get(questionId=1)
        max_length = question._meta.get_field('text').max_length
        self.assertEquals(max_length, 255)

    def test_text_label(self):
        question = Question.objects.get(questionId=1)
        field_label = question._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_quiz_label(self):
        question = Question.objects.get(questionId=1)
        field_label = question._meta.get_field('quiz').verbose_name
        self.assertEquals(field_label, 'quiz')

    def test_object_name_is_name(self):
        question = Question.objects.get(questionId=1)
        expected_object_name = f'{question.text}'
        self.assertEquals(expected_object_name, str(question))

class OptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        student=User.objects.create(username='TestUserStudent', email='testsuser@test.com', name='Bobs', is_student=True,character=character)
        teacher=User.objects.create(username='TestUserTeacher', email='testtuser@test.com', name='Bobt', is_teacher=True)
        course=Class.objects.create(name='TestClass')
        course.teacher.add(teacher)
        course.student.add(student)
        course.save()
        quiz=Quiz.objects.create(name="TestQuiz",teacher=teacher,description="Test quiz model",due_date=timezone.now())
        quiz.course.add(course)
        quiz.save()
        question=Question.objects.create(text="QuestionText", quiz=quiz)
        Option.objects.create(text="OptionText",question=question)

    def test_is_correct_label(self):
        option = Option.objects.get(optionId=1)
        field_label = option._meta.get_field('is_correct').verbose_name
        self.assertEquals(field_label, 'is correct')

    def test_optionId_label(self):
        option = Option.objects.get(optionId=1)
        field_label = option._meta.get_field('optionId').verbose_name
        self.assertEquals(field_label, 'id')

    def test_text_length(self):
        option = Option.objects.get(optionId=1)
        max_length = option._meta.get_field('text').max_length
        self.assertEquals(max_length, 255)

    def test_text_label(self):
        option = Option.objects.get(optionId=1)
        field_label = option._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_object_name_is_name(self):
        option = Option.objects.get(optionId=1)
        expected_object_name = f'{option.text}'
        self.assertEquals(expected_object_name, str(option))

class QuizTakerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        character= Character.objects.create()
        student=User.objects.create(username='TestUserStudent', email='testsuser@test.com', name='Bobs', is_student=True,character=character)
        teacher=User.objects.create(username='TestUserTeacher', email='testtuser@test.com', name='Bobt', is_teacher=True)
        course=Class.objects.create(name='TestClass')
        course.teacher.add(teacher)
        course.student.add(student)
        course.save()
        quiz=Quiz.objects.create(name="TestQuiz",teacher=teacher,description="Test quiz model",due_date=timezone.now())
        quiz.course.add(course)
        quiz.save()
        QuizTaker.objects.create(user=student,quiz=quiz,course=course,quizDueDate=timezone.now())

    def test_object_name_is_name(self):
        taker = QuizTaker.objects.all()[0]
        expected_object_name = f'{taker.user.name}'
        self.assertEquals(expected_object_name, str(taker))

    def test_user_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
    
    def test_quiz_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('quiz').verbose_name
        self.assertEquals(field_label, 'quiz')

    def test_course_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('course').verbose_name
        self.assertEquals(field_label, 'course')

    def test_correct_answer_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('correctAnswers').verbose_name
        self.assertEquals(field_label, 'correctAnswers')
    
    def test_quizDueDate_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('quizDueDate').verbose_name
        self.assertEquals(field_label, 'quizDueDate')

    def test_correct_answer_label(self):
        taker = QuizTaker.objects.all()[0]
        field_label = taker._meta.get_field('timestamp').verbose_name
        self.assertEquals(field_label, 'timestamp')