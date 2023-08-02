from django.urls import path
from .views.college_views import CreateCollege, CollegeList, CollegeAndAdminList

urlpatterns = [
    path("create/", CreateCollege.as_view(), name="college-create"),
    path("college-list/", CollegeList.as_view(), name="college-list"),
    path(
        "college-and-admin-list/",
        CollegeAndAdminList.as_view(),
        name="college-and-admin-users",
    ),
]
