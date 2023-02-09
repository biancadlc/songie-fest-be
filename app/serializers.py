from rest_framework import serializers
from django.db.models import fields
from .models import User, MusicPost, Song, Comment
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model


# fields included in serializer --> what data is returned in API response
class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ['id', 'email', 'username','password', 'date_published', 'first_name', 'last_name',]
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'first_name': {'write_only': True, 'required': True},
                        'last_name': {'write_only': True, 'required': True}}
    def create(self, validated_data):
        # User = get_user_model()
        user = User.objects.create(**validated_data)
        #code with tim version
        # user = User(**validated_data)
        # password = self.validated_data['password']
        # user.set_password(password)
        # user.save()
        # Token.objects.create(user=user)
        return user
        
        

class MusicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicPost
        fields = ('id', 'username', 'date_published', 'likes_count', 'user')
        

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'play_count')
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'date_published')






