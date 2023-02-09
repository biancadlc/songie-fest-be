
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .. models import  MusicPost
from ..serializers import  MusicPostSerializer

from django.contrib.auth import get_user_model

# ==========================================================
#        /explore/     ROUTE           
# ========================================================== 
# user has to be logged in (pass token in header) to view music posts
# GET all music posts, create a music post

@api_view(['GET',])
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
            #checks if username is in dictionary and if not starts with fresh list
            # data[username] = []
            post = {}
            post['date'] = music_post_dict['date_published'].__str__().split(' ')[0]
            post['likes_count'] = music_post_dict['likes_count']
            post['songs'] = []
            for song in music_post.songs.all():
                song_info = {
                    'title': song.title,
                    'artist': song.artist,
                    'play_count': song.play_count
                    }
                post['songs'].append(song_info)
            data[username].append(post)
        # serializer = MusicPostSerializer(music_posts, many=True)
        # return Response(serializer.data)
        return Response(data)


    elif request.method == 'POST':
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)