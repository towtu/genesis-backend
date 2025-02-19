from django.shortcuts import render
from api.models import User, Profile, Todo
from api.serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, TodoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from django.conf import settings
from django.middleware.common import MiddlewareMixin
from corsheaders.middleware import CorsMiddleware

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

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        context = f"Hey {request.user.username}, Welcome to your dashboard"
        return Response({'response': context}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data  # Use request.data to handle JSON
        text = data.get('text', '')

        context = f"Hey {request.user.username}, You posted: {text}"
        return Response({'response': context}, status=status.HTTP_200_OK)

    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class TodoListViews(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

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
