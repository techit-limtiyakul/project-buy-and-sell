import os

from django.db import models
from django.dispatch import receiver

# Create your models here.

class Picture(models.Model):
	picture = models.ImageField(upload_to = 'pictures/')
	#listingKey = models.ForeignKey((...)

@receiver(models.signals.post_delete, sender=Picture)
def DeleteImageFile(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)