from django.urls import path
from .views.college_views import CreateCollege

urlpatterns = [
    path("create/", CreateCollege.as_view(), name="college-create"),
]
