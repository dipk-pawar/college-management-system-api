from django.contrib import admin
from .models import College, Role, Course, CollegeGroup
from django.contrib.auth.models import Group

# Register your models here.
admin.site.register(College)
admin.site.register(Role)
admin.site.register(Course)
admin.site.register(CollegeGroup)
admin.site.unregister(Group)
