
from django.contrib import admin
from . import models
from django import forms

# Register your models here.
admin.site.register(models.QuizCategory)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display=['question','level']
admin.site.register(models.QuizQuestion,QuizQuestionAdmin)


class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display=['id','question','user','right_answer']
admin.site.register(models.UserSubmittedAnswer,UserSubmittedAnswerAdmin)






