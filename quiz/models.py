from django.db import models
from django.template.defaultfilters import slugify

# Quiz Model
class Quiz(models.Model):
    name = models.CharField(unique=True, max_length=50)
    # Course represents class model
    #course = models.ManyToManyField(Class)
    description = models.CharField(max_length=255)
    due_date = models.DateTimeField(auto_now_add=False)
    question_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        # Fix pluralization of model name
        verbose_name_plural = 'Quizzes'
    
# Question model
class Question(models.Model):
    text = models.CharField(unique=True, max_length=50)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    '''
    # Increment question counter on associated quiz
    def save(self, *args, **kwargs):
        self.quiz.question_count +=1
        super(Question, self).save(*args, **kwargs)
    '''
     
    def __str__(self):
        return self.text
    
# Option Model
class Option(models.Model):
    text = models.CharField(unique=True, max_length=50)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# QuizTaker model
class QuizTaker(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correctAnswers = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.user