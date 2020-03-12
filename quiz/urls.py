from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [
        path('', views.user_login, name="index"),

        ]
