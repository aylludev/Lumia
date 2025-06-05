from django.urls import path
from communication.views import ListMessagesView, CreateMessageView, ListSentMessagesView, ReportCreateView
from communication.views import direct_chat_view

urlpatterns = [
    path('profile/messages',ListMessagesView.as_view(), name='messages'),
    path('profile/messages/create/', CreateMessageView.as_view(), name='create_message'),
    path('profile/messages/sent/', ListSentMessagesView.as_view(), name='sent_messages'),
    path('chat/<str:username>/', direct_chat_view, name='direct_chat'),
    path('profile/messages/report/<int:pk>/', ReportCreateView.as_view(), name='report_story'),
]
