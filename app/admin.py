

from django.contrib import admin
from .models import User, Song, Comment, MusicPost

# Register your models here.
admin.site.register(User)
admin.site.register(MusicPost)
admin.site.register(Song)
admin.site.register(Comment)


# === revising comment ==== #

admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'music_post', 'date_published')
    list_filter = ('date_published', 'date_modified')
    search_fields = ('username', 'body')