from django import forms
from django.forms import ModelForm
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'phone'
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Ingrese sus nombres',}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Ingrese sus apellidos',}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Ingrese su email',}
            ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Ingrese su username',}
            ),
            'password': forms.PasswordInput(
                render_value=True,
                attrs={'placeholder': 'Ingrese una contraseña',}
            ),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Ingrese numero de telefono',}
            ),

        }

        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Correo elctrónico',
            'username':'Nombre de Usuario',
            'password':'Contraseña',
            'phone':'Telefono',

        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña
        if commit:
            user.save()
        return user    

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'email', 'username', 'image'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'image': forms.FileInput(),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']

