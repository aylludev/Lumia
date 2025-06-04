from django.contrib import admin
from stories.models import Category, Story, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Story)
admin.site.register(Comment)
