from django.urls import path
from . import views

"""
URL маршруты для приложения users.

Эндпоинты:
- /register/ - регистрация нового пользователя
- /confirm/ - подтверждение пользователя по коду
- /login/ - авторизация пользователя
"""

app_name = 'users'

urlpatterns = [
    # Регистрация пользователя
    path('register/', views.register_user, name='register'),
    
    # Подтверждение пользователя по коду
    path('confirm/', views.confirm_user, name='confirm'),
    
    # Авторизация пользователя
    path('login/', views.login_user, name='login'),
]