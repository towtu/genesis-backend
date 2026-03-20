from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Todo
from .serializers import RegisterSerializer, UserSerializer, TodoSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    return Response({
        'response': f'Welcome back, {user.first_name or user.username}!',
        'user': UserSerializer(user).data,
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        completed_param = request.query_params.get('completed')
        if completed_param is not None:
            todos = todos.filter(completed=completed_param.lower() == 'true')
        search_param = request.query_params.get('search')
        if search_param:
            todos = todos.filter(title__icontains=search_param)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
    except Todo.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TodoSerializer(todo).data)

    if request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def todo_completed(request, pk):
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
    except Todo.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    todo.completed = not todo.completed
    if todo.completed:
        todo.status = 'completed'
    todo.save()
    return Response(TodoSerializer(todo).data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def todo_important(request, pk):
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
    except Todo.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    todo.mark_as_important = not todo.mark_as_important
    todo.save()
    return Response(TodoSerializer(todo).data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if request.method == 'GET':
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': getattr(user, 'bio', ''),
            'verified': getattr(user, 'is_active', False),
        })

    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.save()
    return Response({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': getattr(user, 'bio', ''),
        'verified': getattr(user, 'is_active', False),
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_username(request):
    from .models import User
    new_username = request.data.get('username')
    if not new_username:
        return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
        return Response({'detail': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.username = new_username
    request.user.save()
    return Response({'detail': 'Username changed successfully.'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({'detail': 'Both current and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(current_password):
        return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({'detail': 'New password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Password changed successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_stats(request):
    from django.utils import timezone
    todos = Todo.objects.filter(user=request.user)
    now = timezone.now()
    completed = todos.filter(completed=True).count()
    in_progress = todos.filter(status='in_progress', completed=False).count()
    overdue = todos.filter(due_date__lt=now, completed=False).count()
    return Response({
        'completed': completed,
        'inProgress': in_progress,
        'overdue': overdue,
    })
