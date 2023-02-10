
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .. models import  MusicPost, User
from ..serializers import  MusicPostSerializer
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

# ==========================================================
#        /explore/     ROUTE           
# ========================================================== 
# user has to be logged in (pass token in header) to view music posts
# GET all music posts, create a music post


# UNCOMMENT THIS INCASE OF EMERGENCY
# post_data = [{
    
#         'user': 1,
#         'username': 'ericgarcia',
#         'likes_count': 9,
#         },
#         {
#         'user': 2,
#         'username': 'yamaxu',
#         'likes_count': 4,
#         },

#         {
#         'user': 3,
#         'username': 'biancadlc',
#         'likes_count': 3,
#         },
#         {
#         'user': 4,
#         'username': 'shelbyw',
#         'likes_count': 2,
#         },
        

# ]

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
            #checks if username is in dictionary and if not starts with fresh list
            # data[username] = []
            post = {}
            post['id'] = music_post_dict['id']
            post['date'] = music_post_dict['date_published'].__str__().split(' ')[0]
            post['likes_count'] = music_post_dict['likes_count']
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

    # USE THIS TO QUICKLY RECOVER DATABASE CONTENT
    # UNCOMMENT THIS INCASE OF EMERGENCY
    # elif request.method == 'POST':
    #     for post in post_data:
    #         serializer = MusicPostSerializer(data=post)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,
    #                     status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'POST':
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)