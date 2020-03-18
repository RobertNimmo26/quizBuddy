from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from quiz.models import Quiz, Question, Option, Class, User, QuizTaker, Character
from quiz.forms import UserFormStudent, UserFormTeacher


def about(request):
    context_dict= {}
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'about.html', context=context_dict)

@login_required
def dashboardTeacher(request):
    context_dict = {}
    #Getting the Class and Quiz objects to display
    class_list = Class.objects.all()
    context_dict["classes"] = class_list
    # context_dict["quizes"] = quiz_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    return render(request, 'dashboard-teacher.html', context=context_dict)

def nextQuiz(class_list):
    try:
        quizzes = []
        for c in class_list:
            for q in Quiz.objects.filter(course = c):
                quizzes.append(q)
        nextQuiz = quizzes[0].due_date
        for quiz in quizzes:
            if quiz.due_date < nextQuiz:
                nextQuiz = quiz.due_date
        return nextQuiz
    except:
        return "You have no quizzes!"

@login_required
def dashboardStudent(request):
    context_dict = {}
    #Getting the Class and Quiz objects to display
    class_list = Class.objects.all()
    context_dict["classes"] = class_list

    context_dict['nextQuiz']=nextQuiz(class_list)

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    print(context_dict)
    return render(request, 'dashboard-student.html', context=context_dict)

def manageStudent(request):
    context_dict = {}
    class_list = {}
    #Getting the Class and Quiz objects to display
    print(Class.objects.filter(name='Computing'))
    #RANDOM CODE BITS that were used to add teachers/students to classes for testing purposes
    #request.user.teachers.add(Class.objects.filter(name='Computing').get())
    #User.objects.filter(name='ka').get().students.add(Class.objects.filter(name='Computing').get())
    for teacher_class in request.user.teachers.all():
        student_names = []
        class_name = teacher_class
        print(teacher_class)
        for student in teacher_class.student.all():
            student_names.append(student.name)
        class_list[class_name] = student_names
    context_dict["classes"] = class_list
    # context_dict["quizes"] = quiz_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    return render(request, 'manage-student.html', context=context_dict)

def classList(request, class_name_slug):
    context_dict = {}

    # Gets all class objects
    class_list = request.user.teachers.all()
    context_dict["classes"] = class_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    #Try loop to get all information about class and quiz objects
    try:
        #Getting relevant class object
        #Not using 'class' as keyword
        classObj = Class.objects.get(slug=class_name_slug)
        context_dict['class'] = classObj

        #Getting relevant quiz object
        students = classObj.student.all()
        context_dict['students'] = students

    except Class.DoesNotExist:
        context_dict['students'] = None
        context_dict['class'] = None
    return render(request, 'classList.html', context = context_dict)

@login_required
def show_classStudent(request, class_name_slug):
    print(class_name_slug)
    context_dict = {}

    # Gets all class objects
    class_list = Class.objects.all()
    context_dict["classes"] = class_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    #Try loop to get all information about class and quiz objects
    try:
        #Getting relevant class object
        #Not using 'class' as keyword
        classObj = get_object_or_404(Class,slug=class_name_slug)
        context_dict['class'] = classObj

        #Getting relevant quiz object
        quizzes = Quiz.objects.filter(course = classObj)
        context_dict['quizzes'] = quizzes

        class_list = Class.objects.all()
        context_dict['nextQuiz']=nextQuiz(class_list)

    except Class.DoesNotExist:
        context_dict['quizzes'] = None
        context_dict['class'] = None
    return render(request, 'classStudent.html', context = context_dict)

@login_required
def show_classTeacher(request, class_name_slug):
    context_dict = {}

    # Gets all class objects
    class_list = Class.objects.all()
    context_dict["classes"] = class_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    #Try loop to get all information about class and quiz objects
    try:
        #Getting relevant class object
        #Not using 'class' as keyword
        classObj = get_object_or_404(Class,slug=class_name_slug)
        context_dict['class'] = classObj

        #Getting relevant quiz object
        quizzes = Quiz.objects.filter(course = classObj)
        context_dict['quizzes'] = quizzes

    except Class.DoesNotExist:
        context_dict['quizzes'] = None
        context_dict['class'] = None
    return render(request, 'classTeacher.html', context = context_dict)

@login_required
def preferencesStudent(request):
    #if user is not a student, redirect them to the teachersPreferences
    if request.user.is_student:

        context_dict={}
        #get the user who sent the request
        user = User.objects.get(email = request.user)
        #if its a post method then update the fields
        if request.method == 'POST':
            ableToChange=True

            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['name']:
                user.name = request.POST['name']
            if 'email' in request.POST:
                new_email=request.POST['email']

                for otherUser in User.objects.all():

                    if str(otherUser.email)== str(new_email) and str(new_email)!=str(user.email):
                        context_dict['error']="Email aready exists. Please try a different email."
                        ableToChange=False
                if ableToChange==True:
                    user.email = new_email
            if 'characterType' in request.POST:
                user.character = Character.objects.get(characterType =request.POST['characterType'], evolutionStage = user.evolveScore)
            if request.POST['password']:
                user.set_password(request.POST['password'])
                user.save()
                #ask user to login again
                return redirect('/')

            user.save()
            print(user)
            if ableToChange:
                return redirect('dashboardStudent')

            return render(request, 'preferences-student.html',context_dict)
        return render(request, 'preferences-student.html', context_dict)
    else:
        return redirect('preferencesTeacher')

@login_required
def preferencesTeacher(request):
    if request.user.is_teacher or request.user.is_staff:
        context_dict={}

        user = User.objects.get(email = request.user)
        if request.method == 'POST':
            ableToChange=True

            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['name']:
                user.name = request.POST['name']
            if request.POST['email']:
                new_email=request.POST['email']

                for otherUser in User.objects.all():

                    if str(otherUser.email)== str(new_email) and str(new_email)!=str(user.email):
                        context_dict['error']="Email aready exists. Please try a different email."
                        ableToChange=False
                if ableToChange==True:
                    user.email = new_email
            if request.POST['password']:
                user.set_password(request.POST['password'])
                user.save()
                return redirect('/')
            user.save()

            if ableToChange:
                return redirect('dashboardTeacher')

            return render(request, 'preferences-teacher.html',context_dict)
        return render(request, 'preferences-teacher.html')
    else:
        return redirect('dashboardStudent')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect('/')


def registerStudent(request):
    registered = False

    # means they are trying to register so we have to save the data
    if request.method == 'POST':

        # grabs data from form
        user_form = UserFormStudent(request.POST)

        if user_form.is_valid():
            # save the user's form data to the database
            user = user_form.save()

            # hash the password with the set_password method and update the user object
            user.set_password(user.password)

            user.is_student=True
            user.save()

            registered = True
        else:
            # invalid form, print error
            print(user_form.errors)
    else:
        user_form = UserFormStudent()

    return render(request, 'register-student.html', context = {'user_form': user_form, 'registered': registered})


def registerTeacher(request):
    registered = False

    if request.method == 'POST':

        user_form = UserFormTeacher(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)

            user.is_teacher=True
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserFormTeacher()

    return render(request, 'register-teacher.html', context = {'user_form': user_form, 'registered': registered})


@login_required
def quiz(request,class_name_slug=None,quiz_name_slug=None):

    if request.method =='POST':
        #gets quiz object
        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        correctAnswers=0

        #for each form response checks if answer is true
        for key, value in request.POST.items():
            if value =='True':
                correctAnswers+=1

        #Creates a new quiztaker object
        quiz_taker= QuizTaker(user=request.user,quiz=quiz, correctAnswers=correctAnswers,is_completed=True,)
        quiz_taker.save()

        #calculates new user evolvescore
        currentScore=request.user.evolveScore
        newScore=correctAnswers+currentScore
        request.user.evolveScore=newScore

        #evolves character if points are equal or greater than points required and the user hasn't evolved already
        if (newScore>=70 and request.user.character.evolutionStage!=3):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.characterType, evolutionStage=3)
            character.save()
            request.user.character=character
        elif (newScore>=30 and request.user.character.evolutionStage!=2):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.characterType, evolutionStage=2)
            character.save()
            request.user.character=character
        request.user.save()

        #redirects user to student dashboard
        return redirect(reverse('dashboardStudent'))
    else:
        context_dict = {}

        #gets class object and adds class object to context_dict
        classObj = get_object_or_404(Class,slug=class_name_slug)
        context_dict['class'] = classObj

        #gets quiz object and adds quiz object to context_dict
        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        context_dict['quiz'] = quiz

        #gets all the questions for that quiz
        question_list = Question.objects.filter(quiz = quiz)
        dictOfQuestion={}

        #for each question in the quiz, adds all the options to a temp dict
        for index, question in enumerate(question_list):
                option_list = {Option.objects.filter(question=question_list[index])}
                dictOfQuestion[question]=option_list

        #adds the temp dict of questions and options to context_dict
        context_dict['questions']=dictOfQuestion

        return render(request, 'quiz.html', context=context_dict)


def user_login(request):
    context_dict = {}
    # if post, means they are logging in
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django's auth
        user = authenticate(email=email, password=password)
        # If there's a match
        if user:
            if user.is_active:
                login(request, user)
                if user.is_student:
                    return redirect(reverse('dashboardStudent'))
                else:
                    return redirect('dashboardTeacher')
            else:
                context_dict['error'] = "Your account is disabled."
                return render(request, 'index.html', context=context_dict)
        else:
            # Bad login details were provided
            print(f"Invalid login details: {email}, {password}")
            context_dict['error'] = "Invalid login details supplied."
            return render(request, 'index.html', context=context_dict)

    else:
        return render(request, 'index.html', context=context_dict)
