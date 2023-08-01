# Generated by Django 4.2.3 on 2023-08-01 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0002_alter_role_college'),
        ('accounts', '0010_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='colleges.role'),
            preserve_default=False,
        ),
    ]
