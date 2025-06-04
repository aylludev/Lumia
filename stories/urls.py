from django.urls import path
from stories.views import CreateStoryView, CreateCommentView, UpdateStoryView, like_story

urlpatterns = [
    path('stories/', CreateStoryView.as_view(), name='create_story'),
    path('stories/update/<int:pk>/', UpdateStoryView.as_view(), name='update_story'),
    path('stories/<int:story_id>/comments/', CreateCommentView.as_view(), name='create_comment'),
    path('stories/<int:story_id>/like/', like_story, name='like_story'),
]