from django.urls import path
from communication.views import ListMessagesView, CreateMessageView, ListSentMessagesView, ChatMessageView, ReportCreateView

urlpatterns = [
    path('profile/messages',ListMessagesView.as_view(), name='messages'),
    path('profile/messages/create/', CreateMessageView.as_view(), name='create_message'),
    path('profile/messages/sent/', ListSentMessagesView.as_view(), name='sent_messages'),
    path('profile/messages/chat/<int:pk>/', ChatMessageView.as_view(), name='chat_message'),
    path('profile/messages/report/<int:pk>/', ReportCreateView.as_view(), name='report_story'),
]
