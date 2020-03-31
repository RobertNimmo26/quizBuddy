"""quiz_buddy URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quiz import views

urlpatterns = [ path('', views.user_login, name='index'),
                path('admin/', admin.site.urls),
                path('dashboardStudent/classStudent/<slug:class_name_slug>/',
                    views.show_classStudent, name='classStudent'),
                path('dashboardTeacher/classTeacher/<slug:class_name_slug>/',
                    views.show_classTeacher, name='classTeacher'),
                path('manageStudent/classList/<slug:class_name_slug>/',
                    views.classList, name='classList'),
                path('quiz/', include('quiz.urls')),
                path('about/', views.about, name='about'),
                path('dashboardStudent/', views.dashboardStudent, name='dashboardStudent'),
                path('dashboardTeacher/', views.dashboardTeacher, name='dashboardTeacher'),
                path('manageStudent/', views.manageStudent, name='manageStudent'),
                path('registerStudent/', views.registerStudent, name='registerStudent'),
                path('registerTeacher/', views.registerTeacher, name='registerTeacher'),
                path('dashboardStudent/classStudent/<slug:class_name_slug>/<slug:quiz_name_slug>/',views.quiz,name='quiz'),
                path('user_logout/',views.user_logout,name = 'user_logout'),
                path('preferencesStudent/',views.preferencesStudent, name = 'preferencesStudent'),
                path('preferencesTeacher/', views.preferencesTeacher, name = 'preferencesTeacher'),
                path('createQuiz/', views.createQuiz, name = 'createQuiz'),
                path('quizResultsStudent/',views.quizResultsStudent, name = 'quizResultsStudent'),
                path('quizResultsTeacher/',views.quizResultsTeacher, name = 'quizResultsTeacher'),
                path('quizLibrary/',views.quizLibary, name= 'quizLibrary'),

]
