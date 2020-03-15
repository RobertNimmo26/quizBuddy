from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [
        path('', views.user_login, name="index"),
        path('dashboardStudent/classStudent/<slug:class_name_slug>/<slug:quiz_name_slug>/',views.quiz,name='quiz'),

        ]
