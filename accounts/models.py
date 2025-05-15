from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item
