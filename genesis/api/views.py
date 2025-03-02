from django.db.models import Q
from django.shortcuts import render
from api.models import User, Profile, Todo
from api.serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, TodoSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash

class MyTokenObtainPairview(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        token_serializer = MyTokenObtainPairSerializer()
        token = token_serializer.get_token(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(token.access_token),
                "refresh": str(token),
            },
            status=status.HTTP_201_CREATED,
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        context = f"Hey {request.user.profile.first_name}, Welcome to your Genesis"
        return Response({'response': context}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        text = data.get('text', '')
        context = f"Hey {request.user.profile.first_name}, You posted: {text}"
        return Response({'response': context}, status=status.HTTP_200_OK)
    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class TodoListViews(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        todo_id = self.kwargs['todo_id']
        return Todo.objects.get(id=todo_id, user=self.request.user)

class TodoMarkAsCompleted(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        todo_id = self.kwargs['todo_id']
        todo = Todo.objects.get(id=todo_id, user=self.request.user)
        todo.completed = True
        todo.save()
        return todo

class TodoMarkAsImportant(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        todo_id = self.kwargs['todo_id']
        todo = Todo.objects.get(id=todo_id, user=self.request.user)
        todo.mark_as_important = not todo.mark_as_important
        todo.save()
        return todo

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile = request.user.profile
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class TodoCalendarView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user, due_date__isnull=False)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_stats_view(request):
    user = request.user
    completed = Todo.objects.filter(user=user, completed=True).count()
    in_progress = Todo.objects.filter(user=user, completed=False, due_date__gte=timezone.now()).count()
    overdue = Todo.objects.filter(user=user, completed=False, due_date__lt=timezone.now()).count()

    stats = {
        "completed": completed,
        "inProgress": in_progress,
        "overdue": overdue,
    }
    return Response(stats)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    # Check if the current password is correct
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=400)

    # Validate the new password
    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({"error": e.messages}, status=400)

    # Update the password
    user.set_password(new_password)
    user.save()

    # Update the session to prevent the user from being logged out
    update_session_auth_hash(request, user)

    return Response({"message": "Password changed successfully!"})