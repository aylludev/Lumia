from django.db import models
from accounts.models import CustomUser
from stories.models import Story
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE, verbose_name='Destinatario')
    content = models.TextField(verbose_name='Mensaje')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.timestamp}'

class Report(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField(choices=[
        ('inappropriate_content', 'Contenido Inapropiado'),
        ('spam', 'Spam'),
        ('harassment', 'Acoso'),
        ('copyright_violation', 'Violacion de Derechos de Autor'),
        ('fake_story', 'Historia Falsa'),
        ('other', 'Other')
    ], verbose_name='Motivo')
    content = models.TextField(verbose_name='Descripcion')
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f'Report by {self.reporter.username} on story {self.story.id}'