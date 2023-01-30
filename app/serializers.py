from rest_framework import serializers
from django.db.models import fields
from .models import User, MusicPost, Song, Comment


# fields included in serializer --> what data is returned in API response
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_published')
        
        

class MusicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicPost
        fields = ('id', 'user', 'date_published')
        

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'play_count')
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment', 'date_published')




