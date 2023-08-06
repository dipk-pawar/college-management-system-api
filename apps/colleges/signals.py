from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from django.dispatch import Signal

college_signal = Signal()


@receiver(college_signal)
def custom_signal_receiver(sender, **kwargs):
    if request_data := kwargs.get("request_data"):
        extra_fields = {
            "email": request_data.get("email"),
            "password": request_data.get("password"),
            "first_name": request_data.get("first_name"),
            "last_name": request_data.get("last_name"),
            "college_id": int(request_data.get("college_id")),
            "is_college_admin": True,
        }

        User.objects.create_user(**extra_fields)
