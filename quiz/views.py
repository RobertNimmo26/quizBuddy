from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def dashboardStudent(request):
    return render(request, 'dashboard-student.html')

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
