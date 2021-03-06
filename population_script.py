﻿import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','quiz_buddy.settings')
import django
django.setup()
from django.utils import timezone
from quiz.models import Character,User,Class, Quiz, Question, Option, QuizTaker
from quiz.managers import CustomUserManager

def populate():
    #CREATE USERS AND CHARACTERS
    #------------------------------------------------------------------------------------------------------------------------------------

    student_users = {'Alice':{'email':'alice@test.com', 'username':'alice9','password':'12364','is_student':True, 'character':1,'evolve_score':2},
     'Tom':{'email':'tom@test.com', 'username':'Tom','password':'password','is_student':True,'character':2,'evolve_score':3}}

    teacher_users = {'David':{'email':'david@staff.com', 'username':'david','password':'2856','is_teacher':True,'is_staff':True},
     'Anna':{'email':'anna@testteacher.com', 'username':'anna','password':'anna123','is_teacher':True,'is_staff':True}}

    admin_user = {'Tania':{'email':'tania@admin.com','password':'hello'},
     'Jim':{'email':'jim@admin.com','password':'bye'}}

    characters = [{'type':1,'evolutionStage':1},{'type':1,'evolutionStage':2},{'type':1,'evolutionStage':3},
    {'type':2,'evolutionStage':1},{'type':2,'evolutionStage':2},{'type':2,'evolutionStage':3},
    {'type':3,'evolutionStage':1},{'type':3,'evolutionStage':2},{'type':3,'evolutionStage':3}]

    for c in characters:
        add_character(c['type'],c['evolutionStage'])

    for s, s_data in student_users.items():
        add_student(s,s_data['username'],s_data['email'],s_data['password'],s_data['is_student'],s_data['character'],s_data['evolve_score'])

    for t, t_data in teacher_users.items():
        add_teacher(t,t_data['username'],t_data['email'],t_data['password'],t_data['is_teacher'],t_data['is_staff'])

    for a, a_data in admin_user.items():
        add_admin(a_data['email'],a_data['password'],a)


    #CREATE CLASSES AND ADD QUIZZES TO THE CLASSES
    #------------------------------------------------------------------------------------------------------------------------------------
    math_quiz = [{'name':'MCQSet1', 'description':'A quiz that covers basic arithmetic operations','question_count':3, 'teacher':teacher_users['Anna']},
        {'name': 'MCQSet2' ,'description':'Covers basic geometry questions' , 'question_count':4, 'teacher':teacher_users['David']}]

    computing_quiz = [{'name':'Programming' , 'description': 'Covers basics of programming', 'question_count': 3, 'teacher':teacher_users['Anna']}]

    psyc_quiz = [{'name': 'Psych-Basics', 'description':'Covers the content covered in lectures','question_count':5, 'teacher':teacher_users['David']}]

    course = {'Maths': {'quiz':math_quiz, 'teacher':teacher_users['David'],'student': student_users['Alice']},
     'Computing': {'quiz':computing_quiz,'teacher':teacher_users['Anna'],'student':student_users['Tom']},
      'Psychology':{'quiz':psyc_quiz,'teacher':teacher_users['David'], 'student':student_users['Alice']}}

    quizTaker = {'MCQSet1':{'student':student_users['Alice'],'class':'Maths','correctAns':3,'is_completed':True},
    'Programming':{'student':student_users['Tom'],'class':'Computing','correctAns':2,'is_completed':True}}

    #Add courses and quizzes to courses
    for course, course_data in course.items():
        c = add_class(course,course_data['student']['email'],course_data['teacher']['email'])
        for q in course_data['quiz']:
            add_quiz(c,q['name'],q['description'],q['question_count'],course_data['teacher']['email'])

    #Make students do quizzes
    for q,q_taker in quizTaker.items():
        q = add_quizTaker(q_taker['student']['email'],q,q_taker['class'],q_taker['correctAns'],q_taker['is_completed'])

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
    'options':[{'text':'#','is_correct':True},{'text':'@@','is_correct':False},{'text':'\\','is_correct':False}]}]

    psych_basics = [{'text': 'Pavlov is famous for conducting experiments on ?',
    'options':[{'text': 'Birds','is_correct': False},{'text':'Rats','is_correct':False},{'text':'Dogs','is_correct':True}]},
    {'text':'What area of psychology is Piaget famous for providing theories?',
    'options':[{'text': 'Sexuality','is_correct':False},{'text':'Child Development','is_correct':True},{'text':'Aging','is_correct':False}]},
    {'text':'The first step of classical conditioning is pairing a neutral stimulus with an _____ stimulus.',
    'options':[{'text':'Conditioned','is_correct':False},{'text':'Unconditioned','is_correct':True},{'text':'Novel','is_correct':False}]},
    {'text':'What is the main difference between a psychologist and a psychiatrist?',
    'options':[{'text':'A psychiatrist is classified as a medical doctor','is_correct':True},
    {'text':'A pschologist only holds Associate Degree','is_correct':False},{'text':'Both are the same','is_correct':False}]},
    {'text':'Psychology is the study of mind and ____',
    'options':[{'text':'behaviour','is_correct':True},{'text':'body','is_correct':False},{'text':'Dont Know','is_correct':False}]}]

    quiz__ques = {'MCQSet1':{'questions':questions1},'MCQSet2':{'questions':questions2},
    'Programming':{'questions':programming},'Psych-Basics':{'questions':psych_basics}}

    for quiz, ques in quiz__ques.items():
        for q in ques['questions']:
            add_ques(quiz,q['text'])
            for opt in q['options']:
                add_option(q,opt['text'],opt['is_correct'])

    #PRINT
    #----------------------------------------------------------------------------------------------------------------------------------
    print('\nAdmins')
    print('--------------------')
    for admin in User.objects.filter(is_superuser = True):
        print(f'{admin.name}:{admin}')

    print('\nTeachers')
    print('--------------------')
    for teacher in User.objects.filter(is_teacher = True):
        print(f'{teacher.name}:{teacher}')

    print('\nCharacters...')
    print('--------------------')
    for charac in Character.objects.all():
        print(f' Character:{charac} Evolution Stage:{charac.evolutionStage}')

    print('\nStudents')
    print('--------------------')
    for student in User.objects.filter(is_student = True):
        print(f'Name:{student.name} Email:{student} CharacterType:{student.character} EvolutionStage:{student.evolveScore}')

    print('\nCourses and Quizzes')
    print('---------------------')

    # Print out the classes we have added.
    for c in Class.objects.all():
        for (k,v) in zip(c.teacher.all(),c.student.all()):
            print(f'Course: {c} Teacher: {k} Student: {v}')
        for q in Quiz.objects.filter(course=c):
            print(f'\nCourse: {c}: Quiz: {q} Due Date: {q.due_date}')
            print('-----------------')
            for ques in Question.objects.filter(quiz = q):
                print(f'Question: {ques}')
                for opt in Option.objects.filter(question = ques):
                    print(f'  Option: {opt}')

    print('\nStudent Quiz Scores')
    print('---------------------')
    for q in QuizTaker.objects.all():
        print(f'Student: {q.user.name}, Quiz: {q.quiz}, Complete: {q.is_completed} Correct Answers: {q.correctAnswers}')

    #-----------------------------------------------------------------------------------------------------------------------------------

def add_student(name,username,email,password,is_student,charac,evol_score):
    charact = Character.objects.get(characterType = charac,evolutionStage = evol_score)
    u = User.objects.create_user(email = email, password = password, name = name,
                                                username = username,is_student = is_student,character = charact,evolveScore = evol_score )
    u.save()
    return u

def add_teacher(name,username,email,password,is_teacher,is_staff):
    u = User.objects.create_user(email = email, password = password, name = name,
                                                username = username, is_teacher = is_teacher, is_staff = is_staff )
    u.save()
    return u

def add_admin(email,password,name):
    admin = User.objects.create_superuser(email = email,password = password, name = name)
    admin.save()
    return admin


def add_class(name, s, t):
    c = Class.objects.get_or_create(name=name)[0]
    c.save()
    c.student.add(User.objects.get(email = s))
    c.teacher.add(User.objects.get(email = t))
    return c

def add_quiz(c,name,desc,ques_count,teacher):
    randomDay=random.randint(-5,20)
    date_time = timezone.now() + timezone.timedelta(days=randomDay)
    get_teacher = User.objects.get(email = teacher)

    q = Quiz.objects.get_or_create(name = name,description=desc,due_date=date_time,question_count=ques_count,teacher=get_teacher)[0]
    q.save()
    q.course.add(c)
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

def add_character(charac_type, evolStage ):
    charac = Character.objects.get_or_create(characterType= charac_type, evolutionStage = evolStage)[0]
    charac.save()
    return charac

def add_quizTaker(user,q,course,correctAns,complete):
    quiz = Quiz.objects.get(name = q)
    courseObj = Class.objects.get(name=course)
    student = User.objects.get(email = user)
    quizTaker = QuizTaker.objects.get_or_create(quiz = quiz, user = student,course=courseObj, correctAnswers = correctAns, is_completed = complete, quizDueDate=quiz.due_date)[0]
    quizTaker.save()
    return quizTaker

if __name__ == '__main__':
    print('Starting Quiz population script...')
    populate()
