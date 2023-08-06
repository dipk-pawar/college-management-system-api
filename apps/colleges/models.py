from django.db import models
from django.contrib.auth.models import Group


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
    college = models.ForeignKey("colleges.College", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)
    college = models.ForeignKey(
        "colleges.College", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "college")


class CollegeGroup(Group):
    group_name = models.CharField(max_length=100, blank=False, null=False)
    college = models.ForeignKey("colleges.College", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = "college_group"
        unique_together = (
            "college",
            "group_name",
        )


class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey("colleges.Course", on_delete=models.CASCADE)
    college = models.ForeignKey("colleges.College", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
