from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from api import views


urlpatterns = [
    path('token/', views.MyTokenObtainPairview.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('dashboard/', views.dashboard),
    path('todo/', views.TodoListViews.as_view()),
    path('todo-detail/<int:todo_id>/', views.TodoDetailViews.as_view()),
    path('todo-completed/<int:todo_id>/', views.TodoMarkAsCompleted.as_view()),
    path('profile/', views.profile_view, name='profile'),
    path('todo-important/<int:todo_id>/', views.TodoMarkAsImportant.as_view(), name='todo-mark-as-important'),
    path('calendar-todos/', views.TodoCalendarView.as_view(), name='calendar-todos'),
    path('tasks/stats/', views.task_stats_view, name='task-stats'),
    path('change-password/', views.change_password, name='change-password'),    
]