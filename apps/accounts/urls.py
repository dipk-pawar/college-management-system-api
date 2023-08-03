from django.urls import path
from .views.user_views import Login, RegisterUser
from rest_framework.routers import DefaultRouter
from .views.group_and_permission_views import CollegeGroupViewSet

router = DefaultRouter()
router.register(r"groups", CollegeGroupViewSet, basename="groups")

urlpatterns = [
    path("login/", Login.as_view(), name="login-user"),
    path("register/", RegisterUser.as_view(), name="register-user"),
] + router.urls
