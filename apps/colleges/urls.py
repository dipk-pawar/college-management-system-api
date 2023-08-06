from django.urls import path
from .views.college_views import (
    CreateCollege,
    CollegeList,
    CollegeAndAdminList,
    CollegeUserList,
)
from .views.student_views import CourseList

# from .views.student_views import
from .views.group_and_permission_views import CollegeGroupViewSet, PermissionListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"groups", CollegeGroupViewSet, basename="groups")

urlpatterns = [
    path("create/", CreateCollege.as_view(), name="college-create"),
    path("college-list/", CollegeList.as_view(), name="college-list"),
    path(
        "college-and-admin-list/",
        CollegeAndAdminList.as_view(),
        name="college-and-admin-users",
    ),
    path(
        "users-list/",
        CollegeUserList.as_view(),
        name="college-user-list",
    ),
    path("permission-list/", PermissionListView.as_view(), name="permission-list"),
    path("courses-list/", CourseList.as_view(), name="course-list"),
] + router.urls
