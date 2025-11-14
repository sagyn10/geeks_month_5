from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import ConfirmationCode
import json


class UserRegistrationTest(APITestCase):
    
    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя"""
        url = reverse('users:register')  # Исправленное имя URL
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('confirmation_code', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        
        # Проверяем, что пользователь создан но неактивен
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)
        
        # Проверяем, что код подтверждения создан
        self.assertTrue(ConfirmationCode.objects.filter(user=user).exists())
    
    def test_user_registration_duplicate_username(self):
        """Тест регистрации с дублированным именем пользователя"""
        # Создаем пользователя
        User.objects.create_user(username='testuser', password='pass')
        
        url = reverse('users:register')
        data = {
            'username': 'testuser',  # Дублированное имя
            'password': 'testpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_confirmation_success(self):
        """Тест успешного подтверждения пользователя"""
        # Создаем неактивного пользователя с кодом подтверждения
        user = User.objects.create_user(
            username='testuser', 
            password='testpass', 
            is_active=False
        )
        confirmation = ConfirmationCode.objects.create(user=user)
        
        url = reverse('users:confirm')
        data = {
            'username': 'testuser',
            'code': confirmation.code
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем, что пользователь стал активным
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        
        # Проверяем, что код подтверждения удален
        self.assertFalse(ConfirmationCode.objects.filter(user=user).exists())
    
    def test_user_confirmation_invalid_code(self):
        """Тест подтверждения с неверным кодом"""
        user = User.objects.create_user(
            username='testuser', 
            password='testpass', 
            is_active=False
        )
        ConfirmationCode.objects.create(user=user)
        
        url = reverse('users:confirm')
        data = {
            'username': 'testuser',
            'code': '999999'  # Неверный код
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_success(self):
        """Тест успешного входа активного пользователя"""
        # Создаем активного пользователя
        user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            is_active=True
        )
        
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_user_login_inactive_user(self):
        """Тест входа неактивного пользователя"""
        user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            is_active=False  # Неактивный пользователь
        )
        
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            is_active=True
        )
        
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'  # Неверный пароль
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
