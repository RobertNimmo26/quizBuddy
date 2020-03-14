import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','quiz_buddy.settings')
import django
django.setup()
from django.utils import timezone
from quiz.models import Class, Quiz, Question, Option

def populate():
    
    #CREATE CLASSES AND ADD QUIZZES TO THE CLASSES
    #------------------------------------------------------------------------------------------------------------------------------------
    math_quiz = [{'name':'MCQSet1', 'description':'A quiz that covers basic arithmetic operations','question_count':3},
        {'name': 'MCQSet2' ,'description':'Covers basic geometry questions' , 'question_count':4}]

    computing_quiz = [{'name':'Programming' , 'description': 'Covers basics of programming', 'question_count': 3}]

    psyc_quiz = [{'name': 'Psych-Basics', 'description':'Covers the content covered in lectures','question_count':5}]

    course = {'Maths': {'quiz':math_quiz}, 'Computing': {'quiz':computing_quiz}, 'Psychology':{'quiz':psyc_quiz}}
    #for every course add a quiz
    for course, course_data in course.items():
        c = add_class(course)
        for q in course_data['quiz']:
            add_quiz(c,q['name'],q['description'],q['question_count'])

    #ADD QUESTIONS TO THE QUIZZES AND THEN ADD OPTIONS TO THE QUESTIONS
    #------------------------------------------------------------------------------------------------------------------------------------
    questions1 = [{'text': 'What is 3+8*11 ?',
    'options':[{'text': '121','is_correct': False},{'text':'91','is_correct':True},{'text':'-91','is_correct':False}]},
    {'text':'What is the next number in the series: 2, 9, 30, 93, …?',
    'options':[{'text': '282','is_correct':True},{'text':'102','is_correct':False},{'text':'39','is_correct':False}]},
    {'text':'What is nine-tenths of 2000?',
    'options':[{'text':'2222','is_correct':False},{'text':'1800','is_correct':True},{'text':'20','is_correct':False}]}]

    questions2 = [{'text': 'What is sum of angles in a triangle?',
    'options':[{'text': '360','is_correct': False},{'text':'180','is_correct':True},{'text':'Do not know','is_correct':False}]},
    {'text':'Which triangle has all three equal sides?',
    'options':[{'text': 'Scalene','is_correct':False},{'text':'Isosceles','is_correct':False},{'text':'Equilateral','is_correct':True}]},
    {'text':'How many degrees is a right angle?',
    'options':[{'text':'90','is_correct':True},{'text':'180','is_correct':False},{'text':'0','is_correct':False}]},
    {'text':'How many sides does a hexagon have?',
    'options':[{'text':'7','is_correct':False},{'text':'6','is_correct':True},{'text':'Hexagon does not exits','is_correct':False}]}]

    programming = [{'text':'A syntax error means:',
    'options':[{'text':'Breaking the language rules','is_correct':True},{'text':'Error with the logic','is_correct':False},{'text':'Dont Know','is_correct':False}]},
    {'text':'What symbol is used in Java for "AND"',
    'options':[{'text':'$$','is_correct':False},{'text':'&&','is_correct':True},{'text':'&','is_correct':False}]},
    {'text':'Which symbol is used to denote single line comments in Python',
    'options':[{'text':'#','is_correct':True},{'text':'@@','is_correct':False},{'text':"\\","is_correct":False}]}]

    psych_basics = [{'text': 'Pavlov is famous for conducting experiments on ?',
    'options':[{'text': 'Birds','is_correct': False},{'text':'Rats','is_correct':False},{'text':'Dogs','is_correct':True}]},
    {'text':'What area of psychology is Piaget famous for providing theories?',
    'options':[{'text': 'Sexuality','is_correct':False},{'text':'Child Development','is_correct':True},{'text':'Aging','is_correct':False}]},
    {'text':'The first step of classical conditioning is pairing a neutral stimulus with an _____ stimulus.',
    'options':[{'text':'Conditioned','is_correct':False},{'text':'Unconditioned','is_correct':True},{'text':'Novel','is_correct':False}]},
    {'text':'What is the main difference between a psychologist and a psychiatrist?',
    'options':[{'text':'A psychiatrist is classified as a medical doctor','is_correct':True},{'text':'A pschologist only holds Associate Degree','is_correct':False}]},
    {'text':'Psychology is the study of mind and ____',
    'options':[{'text':'behaviour','is_correct':True},{'text':'body','is_correct':False}]}]

    quiz__ques = {'MCQSet1':{'questions':questions1},'MCQSet2':{'questions':questions2},
    'Programming':{'questions':programming},'Psych-Basics':{'questions':psych_basics}}

    for quiz, ques in quiz__ques.items():
        for q in ques['questions']:
            add_ques(quiz,q['text'])
            for opt in q['options']:
                add_option(q,opt['text'],opt['is_correct'])

    # Print out the classes we have added.
    for c in Class.objects.all():
        for q in Quiz.objects.filter(course=c):
            print(f'{c}: {q}')
            for ques in Question.objects.filter(quiz = q):
                print(f'-:{ques}')
                for opt in Option.objects.filter(question = ques):
                    print(f'--:{opt}')


def add_class(name):
    c = Class.objects.get_or_create(name=name)[0]
    c.save()
    return c 

def add_quiz(c,name,desc,ques_count):
    date_time = timezone.now() + timezone.timedelta(days=3)
    q = Quiz.objects.get_or_create(name = name,description=desc,due_date=date_time,question_count=ques_count)[0]
    q.course.add(c)
    q.save()
    return q

def add_ques(q,text):
    get_quiz = Quiz.objects.get(name = q)
    ques = Question.objects.get_or_create(quiz = get_quiz,text = text)[0]
    ques.save()
    return ques

def add_option(ques,text,is_correct):
    get_ques = Question.objects.get(text = ques['text'])
    opt = Option.objects.get_or_create(question = get_ques, text = text, is_correct = is_correct)[0]
    opt.save()
    return opt

if __name__ == '__main__':
    print('Starting Quiz population script...')
    populate()


#REFERENCES
#------------------------------------------------------------------------------------------------------------------------------------
#Questions for psychology quiz taken from:
#https://quizpug.com. (2020). Can You Answer 12 Basic Psychology Questions?. [online] Available at: https://quizpug.com/can-you-answer-12-basic-psychology-questions/ [Accessed 7 Mar. 2020].