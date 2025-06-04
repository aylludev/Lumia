from django import forms
from django.forms import ModelForm
from communication.models import Message, Report

class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True

    class Meta:
        model = Message
        fields = ('receiver', 'content')
        widgets = {
            'receiver': forms.Select(attrs={'placeholder': 'Destinatario', 'class': 'form-control custom-select slect2'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        exclude = ['sender', 'timestamp', 'is_read']

class ReportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True

    class Meta:
        model = Report
        fields = ('reason', 'content')
        widgets = {
            'reason': forms.Select(attrs={'placeholder': 'Destinatario', 'class': 'form-control custom-select slect2'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        exclude = ['reporter', 'story', 'created_at', 'is_resolved']