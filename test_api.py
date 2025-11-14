#!/usr/bin/env python3
"""
Тестирование API users приложения
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8003/api/v1/users"

def test_registration():
    """Тест регистрации пользователя"""
    print("=== Тестирование регистрации ===")
    
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser123",
        "password": "password123456"
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('confirmation_code')
        return None
        
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что Django сервер запущен на порту 8003")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def test_confirmation(username, code):
    """Тест подтверждения регистрации"""
    if not code:
        print("Пропускаем тест подтверждения - нет кода")
        return False
        
    print("\n=== Тестирование подтверждения ===")
    
    url = f"{BASE_URL}/confirm/"
    data = {
        "username": username,
        "code": code
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def test_login(username, password):
    """Тест входа в систему"""
    print("\n=== Тестирование входа ===")
    
    url = f"{BASE_URL}/login/"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 200:
            return response.json().get('token')
        return None
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    print("Тестирование API users приложения")
    print("Убедитесь, что Django сервер запущен на порту 8003")
    print()
    
    # Тест полного цикла
    username = "testuser123"
    password = "password123456"
    
    # 1. Регистрация
    code = test_registration()
    
    # 2. Подтверждение
    if code:
        confirmed = test_confirmation(username, code)
        
        # 3. Вход после подтверждения
        if confirmed:
            token = test_login(username, password)
            if token:
                print(f"\n✅ Все тесты прошли успешно! Токен: {token}")
            else:
                print("\n❌ Ошибка при входе")
        else:
            print("\n❌ Ошибка при подтверждении")
    else:
        print("\n❌ Ошибка при регистрации")