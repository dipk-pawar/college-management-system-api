# Generated by Django 4.2.3 on 2023-08-01 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='colleges.college'),
        ),
    ]