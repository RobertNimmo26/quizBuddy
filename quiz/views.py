from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from quiz.models import Class
from quiz.models import Quiz

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
        classObj = Class.objects.get(slug=class_name_slug)
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
        classObj = Class.objects.get(slug=class_name_slug)
        context_dict['class'] = classObj

        #Getting relevant quiz object
        quizzes = Quiz.objects.filter(course = classObj)
        context_dict['quizzes'] = quizzes

    except Class.DoesNotExist:
        context_dict['quizzes'] = None
        context_dict['class'] = None
    return render(request, 'classTeacher.html', context = context_dict)

#@login_required
def preferencesStudent(request):
    context_dict= {}
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'preferences-student.html', context=context_dict)

@login_required
def preferencesTeacher(request):
    return render(request, 'preferences-teacher.html')


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
