from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from stories.models import Story, Comment, Category, Like
from stories.forms import StoryForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from communication.models import Message
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def like_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    like, created = Like.objects.get_or_create(user=request.user, story=story)

    if not created:
        # El usuario ya le había dado like, así que lo quitamos
        like.delete()
    return redirect('create_story')  # o donde debas redirigir

# Create your views here.
class CreateStoryView(CreateView):
    template_name = 'stories/create.html'
    model = Story
    form_class = StoryForm
    success_url = '/stories/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_active = True
        form.instance.created_at = datetime.now()
        messages.success(self.request, 'Historia creada correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.request.GET.get('category')
        if category_id:
            stories = Story.objects.filter(is_active=True, category_id=category_id).order_by('-created_at')
            context['selected_category'] = int(category_id)
        else:
            stories = Story.objects.filter(is_active=True).order_by('-created_at')

        # Anotar cantidad de comentarios y likes
        stories = stories.annotate(
            comment_count=Count('comment'),
            like_count=Count('like')
        )

        # Marcar si el usuario ha dado like a cada historia
        if self.request.user.is_authenticated:
            liked_stories_ids = set(
                Like.objects.filter(user=self.request.user, story__in=stories).values_list('story_id', flat=True)
            )
            for story in stories:
                story.user_liked = story.id in liked_stories_ids

            context['messages'] = Message.objects.filter(receiver=self.request.user).order_by('-timestamp')[:3]
            context['count'] = Message.objects.filter(receiver=self.request.user).count()

        context['stories'] = stories
        context['categories'] = Category.objects.all()
        context['title'] = 'Create Story'
        return context


class UpdateStoryView(UpdateView):
    template_name = 'stories/create.html'
    model = Story
    form_class = StoryForm
    success_url = '/stories/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_active = True
        messages.success(self.request, 'Historia creada correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Story'
        return context

    
class CreateCommentView(LoginRequiredMixin, CreateView):
    template_name = 'stories/comments.html'
    model = Comment
    form_class = CommentForm
    success_url = '/stories/'

    def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.story = Story.objects.get(id=self.kwargs['story_id'])
        form.instance.created_at = datetime.now()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = Story.objects.get(id=self.kwargs['story_id'])
        context['comments'] = Comment.objects.filter(story=self.kwargs['story_id']).order_by('-created_at')
        context['title'] = 'Create Comment'
        return context