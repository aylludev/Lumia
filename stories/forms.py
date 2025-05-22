from django import forms
from django.forms import ModelForm
from stories.models import Story, Comment

class StoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['autofocus'] = True

    class Meta:
        model = Story
        fields = ('description', 'file', 'category')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese una descripción', 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        exclude = ['user', 'is_active', 'created_at', 'updated_at']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese un comentario', 'class': 'form-control'}),
        }
        exclude = ['user', 'story', 'created_at', 'updated_at']