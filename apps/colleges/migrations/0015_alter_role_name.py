# Generated by Django 4.2.3 on 2023-08-06 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0014_alter_course_college_alter_role_college_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
