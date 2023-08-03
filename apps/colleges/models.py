from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator


# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    established_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    college = models.ForeignKey("colleges.college", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    college = models.ForeignKey(
        "colleges.college", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name


class CollegeGroup(Group):
    group_name = models.CharField(max_length=100, blank=False, null=False)
    college = models.ForeignKey("colleges.college", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = "college_group"
        unique_together = (
            "college",
            "group_name",
        )
