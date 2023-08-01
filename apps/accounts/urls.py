from django.urls import path
from .views.user_views import Login, RegisterUser

urlpatterns = [
    path("login/", Login.as_view(), name="login-user"),
    path("register/", RegisterUser.as_view(), name="register-user"),
]
