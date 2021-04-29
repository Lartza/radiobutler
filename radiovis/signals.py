from datetime import datetime, timezone, timedelta

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import ProtectedError

from .models import ImageSlide, TextSlide


@receiver(pre_delete, sender=TextSlide)
@receiver(pre_delete, sender=ImageSlide)
def prevent_slide_deletion(sender, instance, using, **kwargs):
    date_send = instance.sent
    if date_send:
        date_now = datetime.now(timezone.utc)

        if (date_now - date_send) < timedelta(days=21):
            raise ProtectedError('Slides must be stored for 21 days due to legal requirements', instance)
