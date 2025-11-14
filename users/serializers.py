from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterUserSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации новых пользователей.
    Принимает username и password.
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
    def validate_username(self, value):
        """
        Проверяем уникальность имени пользователя
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value


class ConfirmUserSerializer(serializers.Serializer):
    """
    Сериализатор для подтверждения регистрации пользователя.
    Принимает username и 6-значный код подтверждения.
    """
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6, min_length=6)


class LoginUserSerializer(serializers.Serializer):
    """
    Сериализатор для входа в систему.
    Принимает username и password, возвращает токен для активных пользователей.
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """
        Проверяем логин и пароль, а также статус активности пользователя
        """
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Аккаунт не активирован. Подтвердите регистрацию.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Неверные учетные данные")
        else:
            raise serializers.ValidationError("Необходимо указать username и password")
        
        return data


class UserConfirmationSerializer(serializers.Serializer):
    """
    Сериализатор для подтверждения пользователя по коду.
    Принимает email и 6-значный код.
    """
    email = serializers.EmailField(
        help_text='Email адрес пользователя для подтверждения'
    )
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        help_text='6-значный код подтверждения'
    )
    
    def validate_code(self, value):
        """
        Проверяем, что код состоит только из цифр.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Код должен состоять только из цифр.")
        return value


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для авторизации пользователя.
    Принимает email/username и пароль.
    """
    email_or_username = serializers.CharField(
        help_text='Email или username для входа'
    )
    password = serializers.CharField(
        write_only=True,
        help_text='Пароль пользователя'
    )
    
    def validate(self, data):
        """
        Проверяем корректность данных для входа.
        """
        email_or_username = data.get('email_or_username')
        password = data.get('password')
        
        # Пытаемся найти пользователя по email или username
        user = None
        if '@' in email_or_username:
            # Если содержит @, считаем это email
            try:
                user = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                pass
        else:
            # Иначе считаем это username
            try:
                user = User.objects.get(username=email_or_username)
            except User.DoesNotExist:
                pass
        
        if not user:
            raise serializers.ValidationError("Пользователь не найден.")
        
        # Проверяем, что пользователь активен
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не подтвержден. Проверьте код подтверждения.")
        
        # Проверяем пароль
        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль.")
        
        data['user'] = user
        return data