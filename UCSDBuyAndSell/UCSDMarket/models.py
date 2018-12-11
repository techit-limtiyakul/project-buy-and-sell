import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver

# Create your models here.
	
class Listing(models.Model):
    
    def __str__ (self):
        return self.title
	
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    canDeliver = models.BooleanField() # true or false
    condition = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
    contactInformation = models.CharField(max_length=20)
    
    '''
    the context of a listing:
    
        "Title" : "IKEA full size bed",
		"Seller" : "John Doe",
		"Price" : 50,
		"CanDeliver" : True,
		"Condition" : "Used",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888"
    '''

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    listingKey = models.ForeignKey(Listing,on_delete=models.CASCADE)

class Picture(models.Model):
	picture = models.ImageField(upload_to = 'pictures/')
	listingKey = models.ForeignKey(Listing,on_delete=models.CASCADE)

@receiver(models.signals.post_delete, sender=Picture)
def DeleteImageFile(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)
