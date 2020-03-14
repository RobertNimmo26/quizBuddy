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
    return render(request, 'register-student.html')

def registerTeacher(request):
    return render(request, 'register-teacher.html')

def user_login(request):
    context_dict = {}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's auth
        user = authenticate(username=username, password=password)
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
            print(f"Invalid login details: {username}, {password}")
            context_dict['error'] = "Invalid login details supplied."
            return render(request, 'index.html', context=context_dict)
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        return render(request, 'index.html', context=context_dict)
