import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','quiz_buddy.settings')
import django
django.setup()
from rango.models import Class, Quiz, Question, Option, QuizTaker

def populate():
    
    math_quiz = [{'name':'MCQ-Set1', 'description':'A quiz that covers basic arithmetic operations','question_count':5},
        {'name': 'MCQ-Set2' ,'description':'Covers basic geometry questions' , 'question_count':7}]

    computing_quiz = [{'name':'Programming' , 'description': 'Covers basics of programming', 'question_count': 4}]

    psyc_quiz = [{'name': 'Adolescence', 'description':'Covers the contents covered in adolescence lectures','question_count':5},
    {'name': 'Adolescence', 'description':'Covers the contents covered in adolescence lectures','question_count':5}]

    course = {'Maths': {'quiz':math_quiz}, 'Computing': {computing_quiz}, 'Psychology':{'quiz':psyc_quiz}}
    #for every course add a quiz
    for course, course_data in course.items():
        c = add_class(course)
        for q in course_data['quiz']:
            add_quiz(c,q['name'],q['description'],q['question_count'])
#------------------------------------------------------------------------------------------------------------------------------------
    #add questions to the quizzes
    math_ques = 

def add_class(name):
    c = Class.objects.get_or_create(name=name)[0]
    c.save()
    return c 

def add_quiz(c,name,description,question_count):
    q = Quiz.objects.get_or_create(Class = c,name,description,question_count)[0]
    q.save()
    return q

def add_ques(q,text):
    ques = Question.objects.get_or_create(Quiz = q,text = text)
    ques.save()
    return ques

def add_option(ques,text,is_correct):
    opt = Option.objects.get_or_create(Question = ques, text = text, is_correct = is_correct)
    opt.save()
    return opt

if __name__ == '__main__':
    print('Starting Quiz population script...')
    populate()