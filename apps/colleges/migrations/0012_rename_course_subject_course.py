# Generated by Django 4.2.3 on 2023-08-06 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0011_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='Course',
            new_name='course',
        ),
    ]
