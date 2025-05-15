from django.urls import path
from accounts.views import LoginFormView, LogoutView, UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
