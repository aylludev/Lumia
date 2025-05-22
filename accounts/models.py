from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from Lumia.settings import MEDIA_URL, STATIC_URL 

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return'{}{}'.format(STATIC_URL, 'img/user.png')


    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['image'] = self.get_image()
        return item