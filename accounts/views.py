from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView, UpdateView, FormView, DetailView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from Lumia import settings
from accounts.forms import UserForm, UserProfileForm
from accounts.models import CustomUser
from stories.models import Story

# Create your views here.
class LoginFormView(LoginView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context

class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro Usuarios'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile_view.html'
    model = CustomUser
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para ver tu perfil.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi perfil'
        user = self.get_object()
        stories = Story.objects.filter(user_id=user).annotate(comment_count=Count('comment')).order_by('-created_at')
        context['stories'] = stories
        context['entity'] = 'Perfil'
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class PasswordUpdateView(LoginRequiredMixin, FormView):
    model = CustomUser
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class = None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar nueva contraseña'
        return form

