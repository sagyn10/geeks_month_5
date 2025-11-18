from django.urls import path
from . import views

"""
URL маршруты для приложения users.

Эндпоинты:
- /register/ - регистрация нового пользователя (CBV RegisterView)
- /confirm/ - подтверждение пользователя по коду (CBV ConfirmView)
- /login/ - авторизация пользователя (CBV LoginView)
"""

app_name = 'users'

urlpatterns = [
    # Регистрация пользователя (CBV)
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Подтверждение пользователя по коду (CBV)
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    
    # Авторизация пользователя (CBV)
    path('login/', views.LoginView.as_view(), name='login'),
]