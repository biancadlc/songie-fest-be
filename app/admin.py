

from django.contrib import admin
from .models import User, Song, Comment, Like, MusicPost

# Register your models here.
admin.site.register(User)
admin.site.register(MusicPost)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Like)