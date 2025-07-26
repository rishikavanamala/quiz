# main/forms.py

from django import forms
from .models import QuizQuestion,QuizCategory

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['category','question', 'option1', 'option2', 'option3', 'option4', 'right_answer']
# class categoryform(forms.ModelForm):
#     class Meta:
#         fields=['']
   

class CategoryForm(forms.ModelForm):
    class Meta:
        model = QuizCategory
        fields = ['title', 'detail']

