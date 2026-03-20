from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/', views.token_obtain, name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('todo/', views.todo_list, name='todo_list'),
    path('todo-detail/<int:pk>/', views.todo_detail, name='todo_detail'),
    path('todo-completed/<int:pk>/', views.todo_completed, name='todo_completed'),
    path('todo-important/<int:pk>/', views.todo_important, name='todo_important'),
    path('profile/', views.profile, name='profile'),
    path('tasks/stats/', views.task_stats, name='task_stats'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-username/', views.change_username, name='change_username'),
]
