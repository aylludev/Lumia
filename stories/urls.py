from django.urls import path
from stories.views import CreateStoryView, CreateCommentView

urlpatterns = [
    path('stories/', CreateStoryView.as_view(), name='create_story'),
    path('stories/<int:story_id>/comments/', CreateCommentView.as_view(), name='create_comment'),
]