import os

from django.db import models
from django.dispatch import receiver

# Create your models here.

class Picture(models.Model):
	picture = models.ImageField(upload_to = 'pictures/')
	# listingKey = models.ForeignKey((...)
	
# added Listing model at 11/09/2018
class Listing(models.Model):
    
    def __str__ (self):
        return self.title
    listingID = models.IntegerField()
    userID = models.IntegerField()
    # 
    # number in a database
    
    # would the model give each listing a unique id?
    
    # maybe a foreignKey should be added to the model of image so that 
    title = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
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

@receiver(models.signals.post_delete, sender=Picture)
def DeleteImageFile(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)