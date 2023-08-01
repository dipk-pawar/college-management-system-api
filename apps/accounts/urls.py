from django.urls import path
from .views.user_views import Login

urlpatterns = [
    path("login/", Login.as_view(), name="user-login"),
]
