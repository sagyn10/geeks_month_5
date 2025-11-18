from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import transaction
from .models import ConfirmationCode
from .serializers import (
    RegisterUserSerializer,
    ConfirmUserSerializer,
    LoginUserSerializer
)


class RegisterView(APIView):
    """
    API для регистрации новых пользователей.
    POST запрос → создаёт неактивного пользователя и код.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Принимает:
        - username: имя пользователя
        - password: пароль
        
        Возвращает:
        - username: имя зарегистрированного пользователя
        - confirmation_code: 6-значный код для подтверждения
        """
        serializer = RegisterUserSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                with transaction.atomic():
                    # Создаем нового пользователя (неактивного)
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        is_active=False  # Пользователь неактивен до подтверждения
                    )
                    
                    # Создаем код подтверждения
                    confirmation = ConfirmationCode.objects.create(user=user)
                    
                    return Response({
                        'message': 'Пользователь зарегистрирован успешно',
                        'username': username,
                        'confirmation_code': confirmation.code
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'error': 'Ошибка при регистрации пользователя'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmView(APIView):
    """
    API для подтверждения регистрации пользователя.
    POST запрос → активирует пользователя.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Принимает:
        - username: имя пользователя
        - code: 6-значный код подтверждения
        
        Возвращает:
        - message: сообщение об успешном подтверждении
        - username: имя активированного пользователя
        """
        serializer = ConfirmUserSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['code']
            
            try:
                with transaction.atomic():
                    # Ищем пользователя по username
                    user = User.objects.get(username=username, is_active=False)
                    
                    # Проверяем код подтверждения
                    confirmation = ConfirmationCode.objects.get(user=user, code=code)
                    
                    # Активируем пользователя
                    user.is_active = True
                    user.save()
                    
                    # Удаляем использованный код подтверждения
                    confirmation.delete()
                    
                    return Response({
                        'message': 'Аккаунт успешно подтвержден',
                        'username': username
                    }, status=status.HTTP_200_OK)
                    
            except User.DoesNotExist:
                return Response({
                    'error': 'Пользователь не найден или уже активирован'
                }, status=status.HTTP_404_NOT_FOUND)
                
            except ConfirmationCode.DoesNotExist:
                return Response({
                    'error': 'Неверный код подтверждения'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                return Response({
                    'error': 'Ошибка при подтверждении аккаунта'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API для входа в систему.
    POST запрос → логинит только активированного пользователя.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Принимает:
        - username: имя пользователя
        - password: пароль
        
        Возвращает:
        - token: токен аутентификации для активных пользователей
        - user_id: ID пользователя
        - username: имя пользователя
        """
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            try:
                # Создаем или получаем токен для пользователя
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Успешный вход в систему',
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({
                    'error': 'Ошибка при входе в систему'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
