from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from api import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairview.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('dashboard/', views.dashboard),

    path('todo/<user_id>/', views.TodoListViews.as_view()),
    path('todo-detail/<user_id>/<todo_id>/', views.TodoDetailViews.as_view()),
    path('todo-completed/<user_id>/<todo_id>/', views.TodoMarkAsCompleted.as_view()),
]