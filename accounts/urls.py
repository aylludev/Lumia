from django.urls import path
from accounts.views import LoginFormView, LogoutView, UserCreateView, ProfileView, UserUpdateView, PasswordUpdateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', UserUpdateView.as_view(), name='update_profile'),
    path('profile/update/password/<int:pk>/', PasswordUpdateView.as_view(), name='update_password'),

]
