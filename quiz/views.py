from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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

def dashboardStudent(request):
    context_dict = {}
    #Getting the Class and Quiz objects to display
    class_list = Class.objects.all()
    context_dict["classes"] = class_list
    # context_dict["quizes"] = quiz_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    return render(request, 'dashboard-student.html', context=context_dict)

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

    except Class.DoesNotExist:
        context_dict['quizzes'] = None
        context_dict['class'] = None
    return render(request, 'classStudent.html', context = context_dict)

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

def preferences(request):
    context_dict= {}
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'preferences.html', context=context_dict)

@login_required
def preferencesStudent(request):
    #if user is not a student, redirect them to the teachersPreferences
    if request.user.is_student:
        #get the user who sent the request
        user = User.objects.get(email = request.user) 
        #if its a post method then update the fields
        if request.method == 'POST':
            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['name']:
                user.name = request.POST['name']
            if 'email' in request.POST:
                user.email = request.POST['email']
            if request.POST['password']:
                user.set_password(request.POST['password'])
            if 'characterType' in request.POST:
                user.character = Character.objects.get(characterType =request.POST['characterType'], evolutionStage = user.evolveScore)
            user.save()
            return redirect('dashboardStudent')
        return render(request, 'preferences-student.html')
    else:
        return redirect('preferencesTeacher')

@login_required
def preferencesTeacher(request):
    if request.user.is_teacher or request.user.is_staff:
        user = User.objects.get(email = request.user) 
        if request.method == 'POST':
            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['name']:
                user.name = request.POST['name']
            if request.POST['email']:
                user.email = request.POST['email']
            if request.POST['password']:
                user.set_password(request.POST['password'])
            user.save()
            return redirect('dashboardTeacher')
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
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserFormTeacher()

    return render(request, 'register-teacher.html', context = {'user_form': user_form, 'registered': registered})



def quiz(request,class_name_slug=None,quiz_name_slug=None):
    #print(request.user)
    print(request)
    if request.method =='POST':
        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        correctAnswers=0
        for key, value in request.POST.items():
            if value =='True':
                correctAnswers+=1
        quiz_taker= QuizTaker(user=request.user,quiz=quiz, correctAnswers=correctAnswers,is_completed=True,)
        quiz_taker.save()
        currentScore=request.user.evolveScore
        newScore=correctAnswers+currentScore
        request.user.evolveScore=newScore
        if (newScore>=70 and request.user.character.evolutionStage!=3):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.characterType, evolutionStage=3)
            character.save()
            request.user.character=character
        elif (newScore>=30 and request.user.character.evolutionStage!=2):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.characterType, evolutionStage=2)
            character.save()
            request.user.character=character
        request.user.save()
        return redirect(reverse('classStudent',kwargs={'class_name_slug':class_name_slug}))
    else:
        context_dict = {}
        classObj = get_object_or_404(Class,slug=class_name_slug)
        context_dict['class'] = classObj

        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        context_dict['quiz'] = quiz

        question_list = Question.objects.filter(quiz = quiz)
        dictOfQuestion={}
        for index, question in enumerate(question_list):
                option_list = {Option.objects.filter(question=question_list[index])}
                dictOfQuestion[question]=option_list
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
                return redirect(reverse('quiz:index'))
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
