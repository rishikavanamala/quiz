
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from . import models
from django.contrib.auth.decorators import login_required
from .models import UserSubmittedAnswer, QuizQuestion, QuizCategory
from django.db.models import F, Q
from django.http import JsonResponse
from .models import QuizCategory, QuizQuestion 
from django.http import JsonResponse
from .forms import QuestionForm,CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages  # Import messages module for alerts
from . import models
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse

#from .forms import QuizCategoryForm, QuizQuestionForm





# Create your views here.
def homepage(request):
    return render(request,"home.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'signup.html', {'alert_message': 'Password and Confirm Password do not match'})

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'alert_message': 'Username already exists'})

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'alert_message': 'Email already exists'})
        # Create the user if both username and email are unique
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'signup.html')



def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        entry = authenticate(request, username=username, password=password)
        print(username, password)
        if entry is not None:
            login(request, entry)
            if entry.is_staff:  # Check if the user is an admin
                return redirect("admin_dashboard")
            return redirect('all-categories')
        else:
            return HttpResponse("Username or password was wrong")
    return render(request, "login.html")






def logout(request):
    auth_logout(request)
    return redirect('login/')


@login_required
def all_categories(request):
    catData=models.QuizCategory.objects.all()
    return render(request,"allcategory.html",{'data':catData})
@login_required
def category_questions(request, cat_id):
    category = get_object_or_404(models.QuizCategory, id=cat_id)

    # Get the current question ID from session or default to the first question
    current_question_id = request.session.get('current_question_id', None)
    if current_question_id is None:
        question = models.QuizQuestion.objects.filter(category=category).order_by('id').first()
        request.session['current_question_id'] = question.id if question else None
    else:
        question = get_object_or_404(models.QuizQuestion, id=current_question_id)

    return render(request, 'category_questions.html', {'category': category, 'data': question})


@login_required
def submit_answer(request, cat_id, quest_id):
    if request.method == 'POST':
        category = get_object_or_404(models.QuizCategory, id=cat_id)
        selected_option = request.POST.get('option')

        if 'skip' in request.POST:
            # Handle skipping question
            question = models.QuizQuestion.objects.filter(category=category, id__gt=quest_id).order_by('id').first()
            if question:
                quest = get_object_or_404(models.QuizQuestion, id=quest_id)
                user = request.user
                answer = 'Not Submitted'
                models.UserSubmittedAnswer.objects.update_or_create(
                    user=user,
                    question=quest,
                    defaults={'right_answer': answer}
                )
                return render(request, 'category_questions.html', {'category': category, 'data': question})
            else:
                return render(request, 'oops.html')

        if not selected_option:
            question = get_object_or_404(models.QuizQuestion, id=quest_id)
            return render(request, 'category_questions.html', {'category': category, 'data': question, 'error_message': 'Please select an option'})

        quest = get_object_or_404(models.QuizQuestion, id=quest_id)
        user = request.user
        answer = selected_option

        # Check if answer already exists for this question and user
        existing_answer = models.UserSubmittedAnswer.objects.filter(user=user, question=quest).first()
        if existing_answer:
            # Update existing answer
            existing_answer.right_answer = answer
            existing_answer.save()
        else:
            # Create new answer
            models.UserSubmittedAnswer.objects.create(user=user, question=quest, right_answer=answer)

        # Get next question
        next_question = models.QuizQuestion.objects.filter(category=category, id__gt=quest_id).order_by('id').first()
        
        if next_question:
            return render(request, 'category_questions.html', {'category': category, 'data': next_question})
        else:
            return redirect('quiz_results')  # Redirect to results page after all questions are answered

    else:
        return HttpResponse('Method not allowed!')

@login_required
def results(request):
    categories = QuizCategory.objects.all()
    category_results = []
    
    for category in categories:
        user_answers = UserSubmittedAnswer.objects.filter(
            user=request.user,
            question__category=category
        ).select_related('question')
        total_questions = category.quizquestion_set.count()  # Correctly access related questions
        skipped_questions = user_answers.filter(right_answer='Not Submitted').count()
        correct_answers = user_answers.filter(right_answer=F('question__right_answer')).count()
        
        attempted_questions = user_answers.count()
        if attempted_questions > 0:
            percentage_score = (correct_answers / attempted_questions) * 100
        else:
            percentage_score = 0
        
        category_result = {
            'category': category,
            'user_answers': user_answers,
            'total_questions': total_questions,
            'attempted_questions': attempted_questions,
            'skipped_questions': skipped_questions,
            'correct_answers': correct_answers,
            'percentage_score': percentage_score,
        }
        
        category_results.append(category_result)
    
    context = {
        'category_results': category_results,
    }
    
    return render(request, 'results.html', context)



@login_required(login_url='login')
def admin_dashboard(request):
    questions = QuizQuestion.objects.all()
    categories =QuizCategory.objects.all()
    
    q = {'questions':questions,'categories':categories}
    return render(request,"admin_dashboard.html",q)


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after adding question
    else:
        form = QuestionForm()
    
    return render(request, 'add_question.html', {'form': form}) 
    

def update_question(request, pk):
    question = get_object_or_404(QuizQuestion, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return HttpResponse("updated successfully")  # Redirect to success page
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'update_question.html', {'form': form, 'question': question})

def delete_question(request, id):
    question = get_object_or_404(QuizQuestion, id=id)
    if request.method == "POST":
        question.delete()
        messages.success(request, f"Question '{question.question}' has been deleted successfully.")
        # After deletion, render admin dashboard page with updated data
        questions = QuizQuestion.objects.all()
        categories =QuizCategory.objects.all()
        return render(request, "admin_dashboard.html", {'questions': questions, 'categories': categories})

    return render(request, "delete_question.html", {'question': question})



def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'admin_dashboard.html' ) # Redirect to success page
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})

@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(QuizCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        return HttpResponse("Category deleted")  # Redirect to a success page or admin_dashboard

    return render(request, 'delete_category.html', {'category': category})

def update_category(request,pk):
    return HttpResponse("something") 



def show_all_questions(request):
    questions = QuizQuestion.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'show_all_questions.html', context)

