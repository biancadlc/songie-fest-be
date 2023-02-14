
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .. models import  MusicPost, User
from ..serializers import  MusicPostSerializer, UserSerializer
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

# ==========================================================
#        /explore/     ROUTE           
# ========================================================== 
# user has to be logged in (pass token in header) to view music posts
# GET all music posts, create a music post

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def explore_posts(request):
    '''
    List all music posts, or create a new music post
    '''
    if request.method == 'GET':
        data = {}
        for music_post in MusicPost.objects.all():
            music_post_dict = music_post.__dict__

            username = str(music_post_dict['username'])

            data[username] = data.get(username, [])
            post = {}
            post['id'] = music_post_dict['id']
            post['date'] = music_post_dict['date_published'].__str__().split(' ')[0]
            post['likes_count'] = music_post.total_likes()
            post['songs'] = []
            for song in music_post.songs.all():
                song_info = {
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'play_count': song.play_count
                    }
                post['songs'].append(song_info)
            data[username].append(post)
        return Response(data)

    elif request.method == 'POST':
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


# ==========================================================
#        /explore/ <music pk> / likes    ROUTE           
# ========================================================== 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username_likes(request, pk):
    '''
    Send in a request that looks like this to change the likes
    {'likes_count': 9,}
    '''
    try:
        post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = {}
        usernames = []
        for user in post.likes.all():
            usernames.append(str(user))

        data['usernames'] = usernames
        return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_like_count(request, pk):
    '''
    get username count. each time you send a request it changes likecount
    '''
    try:
        post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    data = {}
    data['likes_count'] = post.total_likes()
    serializer = MusicPostSerializer(post,
                                    data=data,
                                    partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)