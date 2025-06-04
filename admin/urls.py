from django.urls import path
from admin.views import AdminDashboardView
urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
]
