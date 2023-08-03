from django.contrib import admin
from .models import College, Role, Course, CollegeGroup

# Register your models here.
admin.site.register(College)
admin.site.register(Role)
admin.site.register(Course)
admin.site.register(CollegeGroup)
