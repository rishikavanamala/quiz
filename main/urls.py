
from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.loginpage, name="login"),
    path('', views.homepage, name="home"),
    path('logout/', views.logout, name="logout"),
    path('all-categories/', views.all_categories, name="all-categories"),
    path('category_questions<int:cat_id>/', views.category_questions, name="category_questions"),
    path('submit_answer/<int:cat_id>/<int:quest_id>/', views.submit_answer, name='submit_answer'),
    path('results/', views.results, name='quiz_results'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('show_all_questions/', views.show_all_questions, name='show_all_questions'),
    path('oops/', views.results, name='oops'),
    path('add_question/', views.add_question, name='add_question'),
    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),
    path('update_question/<int:id>/', views.update_question, name='update_question'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
