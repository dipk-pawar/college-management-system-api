from django.db import models


# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    established_date = models.DateField()
    description = models.TextField()

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
