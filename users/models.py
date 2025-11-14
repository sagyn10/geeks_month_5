from django.db import models
from django.contrib.auth.models import User
import random
import string


from django.db import models
from django.contrib.auth.models import User
import random


class ConfirmationCode(models.Model):
    """
    Модель для хранения кодов подтверждения пользователей.
    Связана с пользователем через OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)  # 6-значный код подтверждения
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """
        Автоматически генерируем 6-значный код при создании
        """
        if not self.code:
            self.code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Код подтверждения для {self.user.username}"
