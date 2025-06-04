from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from communication.models import Message, Report
from stories.models import Story
from communication.forms import MessageForm, ReportForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# Create your views here.
class ListMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'inbox.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.get_queryset()
        context['messages'] = messages
        context['count'] = messages.count()
        context['count_sent'] = Message.objects.filter(sender=self.request.user).count()
        context['is_inbox'] = True
        return context

class CreateMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'create_message.html'  # Corregido el nombre de la plantilla
    success_url = reverse_lazy('messages')  # Redirigir al listado de mensajes después de enviar

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Asignar el usuario actual como remitente
        form.instance.sender = self.request.user
        messages.success(self.request, 'Mensaje enviado correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Enviar Mensaje'
        return context

class ListSentMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'inbox.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.get_queryset()
        context['count'] = Message.objects.filter(receiver=self.request.user).count()
        context['messages'] = messages
        context['count_sent'] = messages.count()
        return context

class ChatMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'view_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']  # ID del otro usuario
        user = self.request.user

        # Consultar mensajes donde el request.user sea sender o receiver
        messages = Message.objects.filter(
            Q(sender=user, receiver_id=user_pk) | Q(sender_id=user_pk, receiver=user)
        ).order_by('timestamp')

        context['messages'] = messages
        context['title'] = 'Chat'
        return context

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'report.html'
    success_url = reverse_lazy('create_story')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.story = Story.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = Story.objects.get(id=self.kwargs['pk'])  # Obtener la historia a reportar
        context['title'] = 'Reportar Historia'
        return context
