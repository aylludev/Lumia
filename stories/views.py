from django.contrib import messages
from django.views.generic import CreateView
from stories.models import Story, Comment, Category
from stories.forms import StoryForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

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
    
        for story in stories:
            story.comment_count = Comment.objects.filter(story=story.id).count()
    
        context['stories'] = stories
        context['categories'] = Category.objects.all()
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