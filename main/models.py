
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class QuizCategory(models.Model):
    title=models.CharField(max_length=100)
    detail=models.TextField(max_length=100)

    class meta:
        verbose_name_plural="categories"


    def __str__(self):
        return self.title
    
class QuizQuestion(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    level = models.CharField(max_length=10, default='easy')
    #time_limit=models.IntegerField()
    #time_limit = models.IntegerField(null=True, blank=True)
    right_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question




class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'User Submitted Answers'

