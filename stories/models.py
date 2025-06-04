from django.db import models
from accounts.models import CustomUser
from Lumia.settings import MEDIA_URL, STATIC_URL
from stories.choices import CATEGORY_CHOICES

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Descripción', max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    file = models.FileField(upload_to='media/%Y/%m/%d', null=True, blank=True, verbose_name='Archivo')
    is_active = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    def is_video(self):
        return self.file.name.endswith(('.mp4', '.webm', '.ogg'))

    def is_image(self):
        return self.file.name.endswith(('.jpg', '.jpeg', '.png', '.gif'))

    def get_file(self):
        if self.file:
            return '{}{}'.format(MEDIA_URL, self.file)
        return None

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Descripción', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.story.description}"
    
    class Meta:
        unique_together = ('user', 'story')