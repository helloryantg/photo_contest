from django.contrib import admin
from .models import Contest, Post, Comment

# Register your models here.
admin.site.register(Contest)
admin.site.register(Post)
admin.site.register(Comment)