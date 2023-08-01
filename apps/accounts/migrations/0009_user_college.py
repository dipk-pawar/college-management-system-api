# Generated by Django 4.2.3 on 2023-08-01 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
        ('accounts', '0008_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='college',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='colleges.college'),
            preserve_default=False,
        ),
    ]
