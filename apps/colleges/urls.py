from django.urls import path
from .views.college_views import CreateCollege, CollegeList, CollegeAndAdminList
from .views.student_views import CollegeUserList

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
]
