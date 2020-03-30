import os
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from quiz.models import Quiz, Question, Option, Class, User, QuizTaker, Character
from quiz.forms import UserFormStudent, UserFormTeacher, quizCreationForm, questionFormset
from collections import defaultdict

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

            user.is_student=True
            user.save()
            print(user)
            print(request.user)
            character= Character(characterType=1, can_change=True, evolutionStage=1)
            character.save()

            user.character=character
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

            user.is_teacher=True
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
                if user.is_student:
                    return redirect(reverse('dashboardStudent'))
                else:
                    return redirect('dashboardTeacher')
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

def about(request):
    context_dict= {}
    if not request.user.is_anonymous:
        user = User.objects.get(email = request.user)
        #IF IT'S A STUDENT then we need this info in order to be able to display the deadline
        if user.is_student:
            class_list = []

            #Getting the Class and Quiz objects to display
            for classObj in Class.objects.all():
                if user.email in classObj.get_students():
                    class_list += [classObj]

            # class_list = Class.objects.all()
            context_dict["classes"] = class_list

            context_dict['nextQuiz']=nextQuiz(class_list,request.user)
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'about.html', context=context_dict)

#Checker functions for logged on students or teachers, used with @user_passes_test()
def teacher_check(user):
    #implement using decorator "@user_passes_test(teacher_check)"
    if user.is_teacher:
        return True
    else:
        return False

def student_check(user):
    #implement using decorator "@user_passes_test(student_check)"
    if user.is_student:
        return True
    else:
        return False

#helper function to get next quiz due date for teacher
def getCurrentQuizzesTeacher(userQuizzes,classObj,user):

    dt=datetime.now()

    #Simulating time
    td = timedelta(days=0)

    dontAddQuiz=False
    quizzes=[]
    for quiz in userQuizzes:


        if quiz.due_date.replace(tzinfo=None) < (dt+td):
            dontAddQuiz=True

        if dontAddQuiz ==False:
            quizzes.append(quiz)
        dontAddQuiz=False

    return quizzes

def nextQuizzes(class_list,user):
    quizzes = {}
    nextQuiz=None
    for c in class_list:
        print(c.name)
        userQuizzes= Quiz.objects.filter(course = c)
        for q in getCurrentQuizzesTeacher(userQuizzes,c,user):
            if nextQuiz==None:
                nextQuiz = q
            elif q.due_date < nextQuiz.due_date:
                nextQuiz = q
        if nextQuiz == None:
            quizzes[c]="There's no quizzes due"
        else:
            quizzes[c]=nextQuiz
        nextQuiz=None

    return quizzes

@login_required
@user_passes_test(teacher_check)
def dashboardTeacher(request):
    context_dict = {}
    #Getting the Class and Quiz objects to display
    class_list = []

    user = User.objects.get(email = request.user)

    #Getting the Class and Quiz objects to display
    for classObj in Class.objects.all():
        if user.email in classObj.get_teachers():
            class_list += [classObj]


    context_dict["classes"] = class_list
    context_dict["quizzes"] =nextQuizzes(class_list,request.user)

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    return render(request, 'dashboard-teacher.html', context=context_dict)

#helper functions to get next quiz due date for student.
def getCurrentQuizzesStudent(userQuizzes,classObj,user):

    dt=datetime.now()

    #Simulating time
    td = timedelta(days=0)

    dontAddQuiz=False
    quizzes=[]
    for quiz in userQuizzes:


        if quiz.due_date.replace(tzinfo=None) > (dt+td):
            print(quiz.name)
            quiz_takers=QuizTaker.objects.filter(course = classObj, quiz=quiz)
            for taker in quiz_takers:
                print(taker.is_completed)
                if taker.user==user and taker.is_completed==True:
                    dontAddQuiz=True
        else:
            dontAddQuiz=True

        if dontAddQuiz ==False:
            quizzes.append(quiz)
        dontAddQuiz=False

    return quizzes

def nextQuiz(class_list,user):
    try:
        quizzes = []
        for c in class_list:
            userQuizzes= Quiz.objects.filter(course = c)
            for i in getCurrentQuizzesStudent(userQuizzes,c,user):
                quizzes.append(i)
        nextQuiz = quizzes[0].due_date
        for quiz in quizzes:
            if quiz.due_date < nextQuiz:
                nextQuiz = quiz.due_date
        return nextQuiz
    except:
        return "You have no quizzes!"


@login_required
@user_passes_test(student_check)
def dashboardStudent(request):
    context_dict = {}
    #Getting the Class and Quiz objects to display

    class_list = []

    user = User.objects.get(email = request.user)

    #Getting the Class and Quiz objects to display
    for classObj in Class.objects.all():
        if user.email in classObj.get_students():
            class_list += [classObj]

    # class_list = Class.objects.all()
    context_dict["classes"] = class_list

    context_dict['nextQuiz']=nextQuiz(class_list,request.user)

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    print(context_dict)
    return render(request, 'dashboard-student.html', context=context_dict)

@login_required
@user_passes_test(teacher_check)
def createQuiz(request):
    if request.method == "GET":
        print(request.user)
    if request.method == "POST":
        # Input data sent from form
        quizForm = quizCreationForm(request.POST)
        questionForms = questionFormset(request.POST)
        # Create quiz objects and then save them to DB
        if quizForm.is_valid():
            # Course is synonymous with class
            course = Class.objects.filter(name=quizForm.cleaned_data['course'])[0]
            quiz = Quiz.objects.get_or_create(
                name=quizForm.cleaned_data['quiz_title'],
                description=quizForm.cleaned_data['quiz_description'],
                due_date=quizForm.cleaned_data['due_date'],
                teacher=request.user)[0]
            quiz.course.add(course)
            quiz.save()
            # Get questions
            if questionForms.is_valid():
                # Get data from each form and save to DB
                for noOfQuestions, q in enumerate(questionForms):
                    question = Question(quiz=quiz, text=q.cleaned_data['question'])
                    question.save()
                    # Retrieve correct answer
                    correct_answer = q.cleaned_data['correct_answer']
                    # Set questions and save to database
                    first_option = Option(text=q.cleaned_data['first_option'], question=question, is_correct=False)
                    if(correct_answer == "first_option"):
                        first_option.is_correct=True
                    first_option.save()
                    second_option = Option(text=q.cleaned_data['second_option'], question=question, is_correct=False)
                    if(correct_answer == "second_option"):
                        second_option.is_correct=True
                    second_option.save()
                    third_option = Option(text=q.cleaned_data['third_option'], question=question, is_correct=False)
                    if(correct_answer == "third_option"):
                        third_option.is_correct=True
                    third_option.save()
                quiz.question_count = noOfQuestions + 1
                quiz.save()
        # Clear forms for redirect
        quizForm = quizCreationForm()
        questionForms = questionFormset()
    else:
        quizForm = quizCreationForm()
        questionForms = questionFormset()
        quizForm.fields['course'].queryset=Class.objects.filter(teacher=request.user)

    context_dict = {
        'questionForms':questionForms,
        'quizCreationForm':quizForm,
    }
    return render(request, 'create-quiz.html', context_dict)

@login_required
def quiz(request,class_name_slug=None,quiz_name_slug=None):

    if request.method =='POST':
        #gets class object
        course= get_object_or_404(Class,classId=class_name_slug)
        print(course)
        #gets quiz object
        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        correctAnswers=0

        #for each form response checks if answer is true
        for key, value in request.POST.items():
            if value =='True':
                correctAnswers+=1

        #Creates a new quiztaker object
        quiz_taker= QuizTaker(user=request.user,quiz=quiz, course=course, correctAnswers=correctAnswers,is_completed=True,)
        quiz_taker.save()

        #calculates new user evolvescore
        currentScore=request.user.evolveScore
        newScore=correctAnswers+currentScore
        request.user.evolveScore=newScore

        #evolves character if points are equal or greater than points required and the user hasn't evolved already
        if (newScore>=70 and request.user.character.evolutionStage!=3):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.can_change, evolutionStage=3)
            character.save()
            request.user.character=character
        elif (newScore>=30 and request.user.character.evolutionStage!=2):
            character= Character(characterType=request.user.character.characterType, can_change=request.user.character.can_change, evolutionStage=2)
            character.save()
            request.user.character=character
        request.user.save()

        #redirects user to student dashboard
        return redirect(reverse('dashboardStudent'))
    else:
        context_dict = {}

        #gets class object and adds class object to context_dict
        classObj = get_object_or_404(Class,slug=class_name_slug)
        context_dict['class'] = classObj

        #gets quiz object and adds quiz object to context_dict
        quiz = get_object_or_404(Quiz,quizId=quiz_name_slug)
        context_dict['quiz'] = quiz

        #gets all the questions for that quiz
        question_list = Question.objects.filter(quiz = quiz)
        dictOfQuestion={}

        #for each question in the quiz, adds all the options to a temp dict
        for index, question in enumerate(question_list):
                option_list = {Option.objects.filter(question=question_list[index])}
                dictOfQuestion[question]=option_list

        #adds the temp dict of questions and options to context_dict
        context_dict['questions']=dictOfQuestion

        return render(request, 'quiz.html', context=context_dict)


@login_required
@user_passes_test(student_check)
def show_classStudent(request, class_name_slug):
    print(class_name_slug)
    context_dict = {}

    # Gets all class objects
    class_list = []

    user = User.objects.get(email = request.user)

    #Getting the Class and Quiz objects to display
    for classObj in Class.objects.all():
        if user.email in classObj.get_students():
            class_list += [classObj]
    context_dict["classes"] = class_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    #Getting relevant class object
    #Not using 'class' as keyword
    classObj = get_object_or_404(Class,slug=class_name_slug)

    #Checking that user is in the class
    if user.email not in classObj.get_students():
        return redirect(reverse('dashboardStudent'))
    else:
        context_dict['class'] = classObj

        #Getting relevant quiz object
        userQuizzes = Quiz.objects.filter(course = classObj)

        context_dict['quizzes'] = getCurrentQuizzesStudent(userQuizzes, classObj,request.user)

        context_dict['nextQuiz']=nextQuiz(class_list,request.user)

        apikey= os.getenv("APIKEY")

        context_dict['apikey']=apikey
    return render(request, 'classStudent.html', context = context_dict)

@login_required
@user_passes_test(teacher_check)
def show_classTeacher(request, class_name_slug):
    context_dict = {}

    # Gets all class objects
    class_list = []

    user = User.objects.get(email = request.user)

    #Getting the Class and Quiz objects to display
    for classObj in Class.objects.all():
        if user.email in classObj.get_teachers():
            class_list += [classObj]

    context_dict["classes"] = class_list
    context_dict["quizzesDue"] =nextQuizzes(class_list,request.user)
    print(context_dict["quizzesDue"])


    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)


    #Getting relevant class object
    #Not using 'class' as keyword
    classObj = get_object_or_404(Class,slug=class_name_slug)

    #Checking that user is in the class
    if user.email not in classObj.get_teachers():
        return redirect(reverse('dashboardTeacher'))
    else:

        context_dict['class'] = classObj


        #Getting relevant quiz object
        userQuizzes = Quiz.objects.filter(course = classObj)
        context_dict['quizzes'] =getCurrentQuizzesTeacher(userQuizzes,classObj,request.user)

    return render(request, 'classTeacher.html', context = context_dict)

@login_required
def manageStudent(request):
    context_dict = {}
    class_list = {}
    #Getting the Class and Quiz objects to display
    print(Class.objects.filter(name='Computing'))
    #RANDOM CODE BITS that were used to add teachers/students to classes for testing purposes
    #request.user.teachers.add(Class.objects.filter(name='Computing').get())
    #User.objects.filter(name='ka').get().students.add(Class.objects.filter(name='Computing').get())
    for teacher_class in request.user.teachers.all():
        student_names = []
        class_name = teacher_class
        print(teacher_class)
        for student in teacher_class.student.all():
            student_names.append(student.name)
        class_list[class_name] = student_names
    context_dict["classes"] = class_list
    # context_dict["quizes"] = quiz_list

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    return render(request, 'manage-student.html', context=context_dict)

@login_required
@user_passes_test(student_check)
def quizResultsStudent(request):
    context_dict = {}
    class_list = []
    for c in request.user.students.all():
        class_list.append(c)
    #upcoming deadline
    context_dict['nextQuiz'] = nextQuiz(class_list,request.user)
    #get the quizzes taken by the users if they are completed
    quiz_taken = QuizTaker.objects.filter(user = request.user,is_completed = True)
    context_dict['quiz_taken'] = quiz_taken
    return render(request, 'quizResults-student.html',context = context_dict )

@login_required
@user_passes_test(teacher_check)
def quizResultsTeacher(request):
    context_dict = {}
    quizList = []
    quizTaken = defaultdict(list)
    average_Score = {}

    #for every class where this user is a teacher
    for c in request.user.teachers.all():
        quiz = Quiz.objects.filter(course = c)
        for q in quiz:
            #add the quiz to the quizList
            quizList.append(q)
    #for every quiz in the quizList
    for q in quizList:
        #get the quizTakers who have taken this quiz
        quizTaker = QuizTaker.objects.filter(quiz = q)
        #sum_ans and count used to calculate average
        sum_ans = 0
        count = 0
        #iterate over the querySet
        for q_taken in quizTaker:
            quizTaken[q_taken.quiz].append(q_taken)
            if q_taken.is_completed:
                sum_ans += q_taken.correctAnswers
                count +=1
        #portion of code to calculate average, but if no one has taken the quiz, prevent division by zero error
        if count != 0:
            average_Score[q.name] = sum_ans/count
        else:
            average_Score[q.name] = count

    context_dict['quizTaken'] = dict(quizTaken)
    context_dict['avg_score'] = average_Score
    return render(request,'quizResults-teacher.html',context = context_dict)

@login_required
def classList(request, class_name_slug):
    context_dict = {}

    #request was sent either to add or to remove someone from class
    if request.method == 'POST':
        #if the ass button was clicked on the page
        #it gets the student's email from the form's input field
        #and adds the student to current class (if they exist)
        #if not, it will create an item in the context_dict indicating an error
        if request.POST.get('button') =="add":
            try:
                print("ADDED TO CLASS: ")
                print(Class.objects.get(slug=class_name_slug))
                print("STUDENT TO BE ADDED: ")
                print(request.POST.get('add_student'))
                email = request.POST.get('add_student')
                student = User.objects.filter(email=email).get()
                student.students.add(Class.objects.get(slug=class_name_slug))

            except User.DoesNotExist:
                    context_dict["remove_error"] = [True];
                    print(context_dict["remove_error"])

        #if the remove button was clicked on the page
        #it gets the student's email from the form (the remove button) and removes it
        #from current class
        else:
            print("REMOVED FROM CLASS: ")
            print(Class.objects.get(slug=class_name_slug))
            print("STUDENT TO BE REMOVED: ")
            print(request.POST.get('button'))
            email = request.POST.get('button')
            student = User.objects.filter(email=email).get()
            student.students.remove(Class.objects.get(slug=class_name_slug))

    # Gets all class objects
    class_list = request.user.teachers.all()
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
        students = classObj.student.all()
        context_dict['students'] = students

    except Class.DoesNotExist:
        context_dict['students'] = None
        context_dict['class'] = None
    return render(request, 'classList.html', context = context_dict)

@login_required
@user_passes_test(student_check)
def preferencesStudent(request):
    context_dict={}
    #get the user who sent the request
    user = User.objects.get(email = request.user)
    class_list = []
    for c in request.user.students.all():
        class_list.append(c)
    #upcoming deadline
    context_dict['nextQuiz'] = nextQuiz(class_list, request.user)
    #if its a post method then update the fields
    if request.method == 'POST':
        ableToChange=True

        if request.POST['username']:
            user.username = request.POST['username']
        if request.POST['name']:
            user.name = request.POST['name']
        if 'email' in request.POST:
            new_email=request.POST['email']

            for otherUser in User.objects.all():

                if str(otherUser.email)== str(new_email) and str(new_email)!=str(user.email):
                    context_dict['error']="Email aready exists. Please try a different email."
                    ableToChange=False
            if ableToChange==True:
                user.email = new_email
        if 'characterType' in request.POST:
            character = Character(characterType=request.POST['characterType'], can_change=request.user.character.can_change, evolutionStage=user.character.evolutionStage)
            character.save()
            user.character = character
        if request.POST['password']:
            user.set_password(request.POST['password'])
            user.save()
            #ask user to login again
            return redirect('/')

        user.save()
        print(user)
        if ableToChange:
            return redirect('dashboardStudent')

        return render(request, 'preferences-student.html',context_dict)
    return render(request, 'preferences-student.html', context_dict)

@login_required
@user_passes_test(teacher_check)
def preferencesTeacher(request):
    context_dict={}

    user = User.objects.get(email = request.user)
    if request.method == 'POST':
        ableToChange=True

        if request.POST['username']:
            user.username = request.POST['username']
        if request.POST['name']:
            user.name = request.POST['name']
        if request.POST['email']:
            new_email=request.POST['email']

            for otherUser in User.objects.all():

                if str(otherUser.email)== str(new_email) and str(new_email)!=str(user.email):
                    context_dict['error']="Email aready exists. Please try a different email."
                    ableToChange=False
            if ableToChange==True:
                user.email = new_email
        if request.POST['password']:
            user.set_password(request.POST['password'])
            user.save()
            return redirect('/')
        user.save()

        if ableToChange:
            return redirect('dashboardTeacher')

        return render(request, 'preferences-teacher.html',context_dict)
    return render(request, 'preferences-teacher.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect('/')
